import numpy as np

from Agents.Household import Household


class MDPHousehold(Household):
    def setup(self):
        """Initialize a new variable at agent creation."""
        super().setup()

        self.action_space = ["buy", "sell", "store", "none"]

        self.state_space = [
            (energy, weather) for energy in [-1, 0, 1] for weather in ["sunny", "cloudy"]
        ]

        # Initialize Q values with zeros
        self.q_values = {}
        for state in self.state_space:
            for action in self.action_space:
                self.q_values[(state, action)] = 0

        # Initialize policy with random actions
        self.policy = {}
        for state in self.state_space:
            self.policy[state] = np.random.choice(self.action_space)

        self.transitions = {}
        for state in self.state_space:
            for action in self.action_space:
                for next_state in self.state_space:
                    self.transitions[(state, action, next_state)] = 0

        self.rewards = {}
        for state in self.state_space:
            for action in self.action_space:
                if action == "buy":
                    self.rewards[(state, action)] = -1
                elif action == "sell":
                    self.rewards[(state, action)] = 1
                elif action == "store":
                    self.rewards[(state, action)] = 0
            
        # Discount factor
        self.gamma = 0.9

    def update_energy(self, sunny):
        super().update_energy(sunny)
        self.current_state = (np.sign(self.energy_bal), sunny)

    def set_status(self):
        super().set_status()

    def energy_decision(self):
        action = self._get_action(self.current_state)


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
                seller.cost += transfered
                self.cost -= transfered * distance

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
                seller.cost += transfered
                self.cost -= transfered * distance

        # Buy from the grid
        else:
            # Transfer
            transfered = abs(self.energy_bal)
            self.grid_trans += transfered
            # Balance
            self.energy_bal = 0
            # Cost
            self.cost -= transfered * 10

    def _get_action(self, state):


    def _policy_iteration(self, states, actions):
        pass

        # Initialize random policy
        # init_policy = {state: random.choice(actions) for state in states}
        # current_depth = 0
        # while current_depth < depth:
        #     # Evaluate current policy
        #     value = self.policy_evaluation(states, actions, delta, init_policy)
        #     current_depth += 1
        #     for i, state in enumerate(states):
        #         pass

    def _policy_evaluation(self, policy, states):
        reward = 0

        # values = {state: 0 for state in states}
        # if depth == 0:
        #     values
        # for current_state in states:
        #     action = policy[current_state]
        #     for next_state in states:
        #         values[current_state] += self._get_transition(current_state, action, next_state) * (
        #             self._get_reward(current_state, action, next_state)
        #             + delta * self._policy_evaluation(policy, states, depth - 1)[next_state]
        #         )

        # return values
