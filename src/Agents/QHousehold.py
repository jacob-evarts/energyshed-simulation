import numpy as np
from node_queue import NodeQueue

from Agents.Household import Household


class QHousehold(Household):
    def setup(self):
        """Initialize a new variable at agent creation."""
        super().setup()

        self.action_space = ["buy", "sell"]

        self.state_space = [(energy, weather) for energy in [-1, 0, 1] for weather in [True, False]]
        self.current_state = None

        # Initialize Q values with zeros
        self.q_values = {}
        for state in self.state_space:
            for action in self.action_space:
                self.q_values[(state, action)] = 0

        # Exploration factor
        self.learning_rate = 0.2
        self.epsilon = 0.1
        self.discount_factor = 0.9

    def update_energy(self, sunny):
        super().update_energy(sunny)
        self.current_state = (np.sign(self.energy_bal), sunny)

    def energy_decision(self):
        self.action = self.choose_action(self.current_state)

        if self.action == "buy":
            self.status = -1
        elif self.action == "sell":
            self.status = 1
        elif self.action == "store":
            self.status = 0

    def buy(self):
        if self.action == "buy":
            self._buy_energy()

    def store(self):
        pass

    def sell(self):
        if self.action == "sell":
            self.daily_cost += self.energy_bal
            self.total_cost += self.daily_cost

    def get_q_value(self, state, action):
        return self.q_values[(state, action)]

    def choose_action(self, state):
        if np.random.uniform(0, 1) < self.epsilon:
            action = np.random.choice(self.action_space)
        else:
            action = self.get_best_action(state)
        return action

    def update_q_values(self, forcast):
        reward = self.get_reward()
        next_state = (np.sign(self.energy_bal), forcast)

        current_q_value = self.get_q_value(self.current_state, self.action)
        next_q_values = [self.get_q_value(next_state, action) for action in self.action_space]
        next_q_value = max(next_q_values)

        sample = reward + self.discount_factor * next_q_value
        new_q_value = (1 - self.learning_rate) * current_q_value + self.learning_rate * sample

        self.q_values[(self.current_state, self.action)] = new_q_value

    def get_q_values(self):
        return dict(self.q_values)

    def get_reward(self):
        reward = 0
        if self.energy_bal < 0:
            reward -= 1000
        reward += self.daily_cost
        return reward

    def get_best_action(self, state):
        best_action = None
        best_q_value = None

        for action in self.action_space:
            q_value = self.get_q_value(state, action)

            if best_q_value is None or q_value > best_q_value:
                best_q_value = q_value
                best_action = action

        return best_action

    def _buy_energy(self):
        seller, distance = self._bfs()
        if seller:
            # Buy all of neighbor's energy
            if abs(self.energy_bal) >= seller.energy_bal:
                # Transfer
                transfered = abs(seller.energy_bal)
                self.local_trans += transfered
                # Balance
                self.energy_bal = self.energy_bal + seller.energy_bal
                seller.energy_bal = 0
                # Cost
                seller.daily_cost += transfered
                seller.total_cost += transfered
                self.daily_cost += -(transfered * distance)
                self.total_cost += self.daily_cost

                if self.energy_bal < 0:
                    self._buy_energy()

            # Buy some of neighbor's energy
            elif abs(self.energy_bal) < seller.energy_bal:
                # Transfer
                transfered = abs(self.energy_bal)
                self.local_trans += transfered
                # Balance
                seller.energy_bal = seller.energy_bal + self.energy_bal
                self.energy_bal = 0
                # Cost
                seller.daily_cost += transfered
                seller.total_cost += transfered
                self.daily_cost += -(transfered * distance)
                self.total_cost += self.daily_cost

        # Buy from the grid
        else:
            # Transfer
            transfered = abs(self.energy_bal)
            self.grid_trans += transfered
            # Balance
            self.energy_bal = 0
            # Cost
            self.daily_cost += -(transfered * 10)
            self.total_cost += self.daily_cost

    def _bfs(self):
        queue = NodeQueue()
        queue.enqueue(self)
        distances = {self: 0}
        while not queue.is_empty():
            parent_node = queue.dequeue()
            for child in self.network.neighbors(parent_node):
                # If the node is a seller, return it
                if child.action == "sell" and child.energy_bal > 0:
                    return child, distances[parent_node] + 1
                if child not in distances:
                    distances[child] = distances[parent_node] + 1
                    queue.enqueue(child)
        return None, None
