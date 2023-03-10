import numpy as np

from Agents.ReflexHousehold import ReflexHousehold


class QHousehold(ReflexHousehold):
    def setup(self):
        """Initialize a new variable at agent creation."""
        super().setup()
        self.storage = 0

        self.action_space = ["buy", "sell", "store"]

        self.state_space = [
            (energy, weather, storage)
            for energy in [-1, 1]
            for weather in ["sun", "clouds"]
            for storage in [0, 1]
        ]
        self.current_state = None

        # Initialize Q values with zeros
        self.q_values = {}
        for state in self.state_space:
            for action in self.action_space:
                self.q_values[(state, action)] = 0

        # Exploration factor
        self.learning_rate = 0.1
        self.epsilon = 0.2
        self.discount_factor = 0.9

    def update_energy(self, weather):
        super().update_energy(weather)
        stored_flag = 0
        # Use stored energy if available
        if self.storage > 0:
            stored_flag = 1
            self.energy_bal = self.energy_bal + self.storage
            self.storage = 0

        energy_status = np.sign(self.energy_bal)
        if energy_status == 0:
            energy_status = 1

        self.current_state = (energy_status, weather, stored_flag)

    def energy_decision(self):
        self.action = self.choose_action(self.current_state)

        if self.action == "buy":
            self.status = -1
        elif self.action == "sell":
            self.status = 1
        elif self.action == "store":
            self.status = 0

    def store(self):
        if self.action == "store":
            if self.energy_bal > 0:
                transfered = self.energy_bal
                self.storage += transfered
                self.energy_bal = 0
            else:
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
        store_flag = 1 if self.storage > 0 else 0
        energy_status = np.sign(self.energy_bal)
        if energy_status == 0:
            energy_status = 1
        next_state = (energy_status, forcast, store_flag)

        current_q_value = self.get_q_value(self.current_state, self.action)
        next_q_values = [self.get_q_value(next_state, action) for action in self.action_space]
        next_q_value = max(next_q_values)

        reward = self.get_reward()
        sample = reward + self.discount_factor * next_q_value
        new_q_value = (1 - self.learning_rate) * current_q_value + self.learning_rate * sample

        self.q_values[(self.current_state, self.action)] = new_q_value

    def get_q_values(self):
        return dict(self.q_values)

    def get_reward(self):
        reward = 0
        if self.energy_bal < 0:
            reward -= 100
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
