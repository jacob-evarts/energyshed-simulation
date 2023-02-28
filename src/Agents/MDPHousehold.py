from Agents.Household import Household


class MDPHousehold(Household):
    def setup(self):
        """Initialize a new variable at agent creation."""
        super().setup()

        self.states = [
            (energy, weather) for energy in [-1, 0, 1] for weather in ["sunny", "cloudy"]
        ]

        self.actions = ["buy", "sell", "none"]

        self.transition_probs = {
            {
                (1, "sunny"): {
                    "buy": {
                        (1, "sunny"): 0.2,
                        (0, "sunny"): 0.2,
                        (-1, "sunny"): 0.2,
                        (1, "cloudy"): 0.2,
                        (0, "cloudy"): 0.1,
                        (-1, "cloudy"): 0.1,
                    },
                    "sell": {
                        (1, "sunny"): 0.1,
                        (0, "sunny"): 0.2,
                        (-1, "sunny"): 0.2,
                        (1, "cloudy"): 0.1,
                        (0, "cloudy"): 0.2,
                        (-1, "cloudy"): 0.2,
                    },
                    "none": {
                        (1, "sunny"): 0.2,
                        (0, "sunny"): 0.2,
                        (-1, "sunny"): 0.2,
                        (1, "cloudy"): 0.2,
                        (0, "cloudy"): 0.2,
                        (-1, "cloudy"): 0.2,
                    },
                },
                (0, "sunny"): {
                    "buy": {
                        (1, "sunny"): 0.2,
                        (0, "sunny"): 0.2,
                        (-1, "sunny"): 0.2,
                        (1, "cloudy"): 0.2,
                        (0, "cloudy"): 0.1,
                        (-1, "cloudy"): 0.1,
                    },
                    "sell": {
                        (1, "sunny"): 0.1,
                        (0, "sunny"): 0.2,
                        (-1, "sunny"): 0.2,
                        (1, "cloudy"): 0.1,
                        (0, "cloudy"): 0.2,
                        (-1, "cloudy"): 0.2,
                    },
                    "none": {
                        (1, "sunny"): 0.2,
                        (0, "sunny"): 0.2,
                        (-1, "sunny"): 0.2,
                        (1, "cloudy"): 0.2,
                        (0, "cloudy"): 0.2,
                        (-1, "cloudy"): 0.2,
                    },
                },
                (-1, "sunny"): {
                    "buy": {
                        (1, "sunny"): 0.2,
                        (0, "sunny"): 0.2,
                        (-1, "sunny"): 0.2,
                        (1, "cloudy"): 0.2,
                        (0, "cloudy"): 0.1,
                        (-1, "cloudy"): 0.1,
                    },
                    "sell": {
                        (1, "sunny"): 0.1,
                        (0, "sunny"): 0.2,
                        (-1, "sunny"): 0.2,
                        (1, "cloudy"): 0.1,
                        (0, "cloudy"): 0.2,
                        (-1, "cloudy"): 0.2,
                    },
                    "none": {
                        (1, "sunny"): 0.2,
                        (0, "sunny"): 0.2,
                        (-1, "sunny"): 0.2,
                        (1, "cloudy"): 0.2,
                        (0, "cloudy"): 0.2,
                        (-1, "cloudy"): 0.2,
                    },
                },
                (1, "cloudy"): {
                    "buy": {
                        (1, "sunny"): 0.2,
                        (0, "sunny"): 0.2,
                        (-1, "sunny"): 0.2,
                        (1, "cloudy"): 0.2,
                        (0, "cloudy"): 0.1,
                        (-1, "cloudy"): 0.1,
                    },
                    "sell": {
                        (1, "sunny"): 0.1,
                        (0, "sunny"): 0.2,
                        (-1, "sunny"): 0.2,
                        (1, "cloudy"): 0.1,
                        (0, "cloudy"): 0.2,
                        (-1, "cloudy"): 0.2,
                    },
                    "none": {
                        (1, "sunny"): 0.2,
                        (0, "sunny"): 0.2,
                        (-1, "sunny"): 0.2,
                        (1, "cloudy"): 0.2,
                        (0, "cloudy"): 0.2,
                        (-1, "cloudy"): 0.2,
                    },
                },
                (0, "cloudy"): {
                    "buy": {
                        (1, "sunny"): 0.2,
                        (0, "sunny"): 0.2,
                        (-1, "sunny"): 0.2,
                        (1, "cloudy"): 0.2,
                        (0, "cloudy"): 0.1,
                        (-1, "cloudy"): 0.1,
                    },
                    "sell": {
                        (1, "sunny"): 0.1,
                        (0, "sunny"): 0.2,
                        (-1, "sunny"): 0.2,
                        (1, "cloudy"): 0.1,
                        (0, "cloudy"): 0.2,
                        (-1, "cloudy"): 0.2,
                    },
                    "none": {
                        (1, "sunny"): 0.2,
                        (0, "sunny"): 0.2,
                        (-1, "sunny"): 0.2,
                        (1, "cloudy"): 0.2,
                        (0, "cloudy"): 0.2,
                        (-1, "cloudy"): 0.2,
                    },
                },
                (-1, "cloudy"): {
                    "buy": {
                        (1, "sunny"): 0.2,
                        (0, "sunny"): 0.2,
                        (-1, "sunny"): 0.2,
                        (1, "cloudy"): 0.2,
                        (0, "cloudy"): 0.1,
                        (-1, "cloudy"): 0.1,
                    },
                    "sell": {
                        (1, "sunny"): 0.1,
                        (0, "sunny"): 0.2,
                        (-1, "sunny"): 0.2,
                        (1, "cloudy"): 0.1,
                        (0, "cloudy"): 0.2,
                        (-1, "cloudy"): 0.2,
                    },
                    "none": {
                        (1, "sunny"): 0.2,
                        (0, "sunny"): 0.2,
                        (-1, "sunny"): 0.2,
                        (1, "cloudy"): 0.2,
                        (0, "cloudy"): 0.2,
                        (-1, "cloudy"): 0.2,
                    },
                },
            }
        }

        self.rewards = {
            {
                (1, "sunny"): {
                    "buy": {
                        (1, "sunny"): 0.2,
                        (0, "sunny"): 0.2,
                        (-1, "sunny"): 0.2,
                        (1, "cloudy"): 0.2,
                        (0, "cloudy"): 0.1,
                        (-1, "cloudy"): 0.1,
                    },
                    "sell": {
                        (1, "sunny"): 0.1,
                        (0, "sunny"): 0.2,
                        (-1, "sunny"): 0.2,
                        (1, "cloudy"): 0.1,
                        (0, "cloudy"): 0.2,
                        (-1, "cloudy"): 0.2,
                    },
                    "none": {
                        (1, "sunny"): 0.2,
                        (0, "sunny"): 0.2,
                        (-1, "sunny"): 0.2,
                        (1, "cloudy"): 0.2,
                        (0, "cloudy"): 0.2,
                        (-1, "cloudy"): 0.2,
                    },
                },
                (0, "sunny"): {
                    "buy": {
                        (1, "sunny"): 0.2,
                        (0, "sunny"): 0.2,
                        (-1, "sunny"): 0.2,
                        (1, "cloudy"): 0.2,
                        (0, "cloudy"): 0.1,
                        (-1, "cloudy"): 0.1,
                    },
                    "sell": {
                        (1, "sunny"): 0.1,
                        (0, "sunny"): 0.2,
                        (-1, "sunny"): 0.2,
                        (1, "cloudy"): 0.1,
                        (0, "cloudy"): 0.2,
                        (-1, "cloudy"): 0.2,
                    },
                    "none": {
                        (1, "sunny"): 0.2,
                        (0, "sunny"): 0.2,
                        (-1, "sunny"): 0.2,
                        (1, "cloudy"): 0.2,
                        (0, "cloudy"): 0.2,
                        (-1, "cloudy"): 0.2,
                    },
                },
                (-1, "sunny"): {
                    "buy": {
                        (1, "sunny"): 0.2,
                        (0, "sunny"): 0.2,
                        (-1, "sunny"): 0.2,
                        (1, "cloudy"): 0.2,
                        (0, "cloudy"): 0.1,
                        (-1, "cloudy"): 0.1,
                    },
                    "sell": {
                        (1, "sunny"): 0.1,
                        (0, "sunny"): 0.2,
                        (-1, "sunny"): 0.2,
                        (1, "cloudy"): 0.1,
                        (0, "cloudy"): 0.2,
                        (-1, "cloudy"): 0.2,
                    },
                    "none": {
                        (1, "sunny"): 0.2,
                        (0, "sunny"): 0.2,
                        (-1, "sunny"): 0.2,
                        (1, "cloudy"): 0.2,
                        (0, "cloudy"): 0.2,
                        (-1, "cloudy"): 0.2,
                    },
                },
                (1, "cloudy"): {
                    "buy": {
                        (1, "sunny"): 0.2,
                        (0, "sunny"): 0.2,
                        (-1, "sunny"): 0.2,
                        (1, "cloudy"): 0.2,
                        (0, "cloudy"): 0.1,
                        (-1, "cloudy"): 0.1,
                    },
                    "sell": {
                        (1, "sunny"): 0.1,
                        (0, "sunny"): 0.2,
                        (-1, "sunny"): 0.2,
                        (1, "cloudy"): 0.1,
                        (0, "cloudy"): 0.2,
                        (-1, "cloudy"): 0.2,
                    },
                    "none": {
                        (1, "sunny"): 0.2,
                        (0, "sunny"): 0.2,
                        (-1, "sunny"): 0.2,
                        (1, "cloudy"): 0.2,
                        (0, "cloudy"): 0.2,
                        (-1, "cloudy"): 0.2,
                    },
                },
                (0, "cloudy"): {
                    "buy": {
                        (1, "sunny"): 0.2,
                        (0, "sunny"): 0.2,
                        (-1, "sunny"): 0.2,
                        (1, "cloudy"): 0.2,
                        (0, "cloudy"): 0.1,
                        (-1, "cloudy"): 0.1,
                    },
                    "sell": {
                        (1, "sunny"): 0.1,
                        (0, "sunny"): 0.2,
                        (-1, "sunny"): 0.2,
                        (1, "cloudy"): 0.1,
                        (0, "cloudy"): 0.2,
                        (-1, "cloudy"): 0.2,
                    },
                    "none": {
                        (1, "sunny"): 0.2,
                        (0, "sunny"): 0.2,
                        (-1, "sunny"): 0.2,
                        (1, "cloudy"): 0.2,
                        (0, "cloudy"): 0.2,
                        (-1, "cloudy"): 0.2,
                    },
                },
                (-1, "cloudy"): {
                    "buy": {
                        (1, "sunny"): 0.2,
                        (0, "sunny"): 0.2,
                        (-1, "sunny"): 0.2,
                        (1, "cloudy"): 0.2,
                        (0, "cloudy"): 0.1,
                        (-1, "cloudy"): 0.1,
                    },
                    "sell": {
                        (1, "sunny"): 0.1,
                        (0, "sunny"): 0.2,
                        (-1, "sunny"): 0.2,
                        (1, "cloudy"): 0.1,
                        (0, "cloudy"): 0.2,
                        (-1, "cloudy"): 0.2,
                    },
                    "none": {
                        (1, "sunny"): 0.2,
                        (0, "sunny"): 0.2,
                        (-1, "sunny"): 0.2,
                        (1, "cloudy"): 0.2,
                        (0, "cloudy"): 0.2,
                        (-1, "cloudy"): 0.2,
                    },
                },
            }
        }

    def update_energy(self, sunny):
        super().update_energy(sunny)

    def set_status(self):
        super().set_status()

    def energy_decision(self):
        # Need to buy energy
        if self.status == -1:
            self._buy_energy()

    def _buy_energy(self):
        # buy energy from neighbor
        for n in self.network.neighbors(self):
            if n.status == "sell":
                # buy all energy neighbor has
                if abs(self.energy_bal) >= n.energy_bal:
                    self.energy_bal = self.energy_bal + n.energy_bal
                    # buy all neighbor energy - track energy transferred
                    n.energy_trans = n.energy_bal
                    n.energy_bal = 0
                    n.status = "none"
                    if self.energy_bal == 0:
                        break

                # buy some of neighbor's energy
                elif abs(self.energy_bal) < n.energy_bal:
                    n.energy_bal = n.energy_bal + self.energy_bal
                    # self bal is xfered - track energy transferred
                    n.energy_trans = abs(self.energy_bal)
                    self.energy_bal = 0
                    self.status = "none"

    def _get_reward(self, state, action, next_state):
        return self.rewards[state][action][next_state]

    def _get_transition(self, state, action, next_state):
        return self.transition_probs[state][action][next_state]

    @staticmethod
    def policy_iteration(states, actions, delta=0.9, depth=3):
        # Initialize random policy
        init_policy = {state: random.choice(actions) for state in states}
        current_depth = 0
        while current_depth < depth:
            # Evaluate current policy
            value = policy_evaluation(states, actions, delta, init_policy)
            current_depth += 1
            for i, state in enumerate(states):
                pass

    @staticmethod
    def policy_evaluation(policy, states, depth, delta=0.9):
        values = {state: 0 for state in states}
        if depth == 0:
            values
        for current_state in states:
            action = policy[current_state]
            for next_state in states:
                values[current_state] += _get_transition(current_state, action, next_state) * (
                    _get_reward(current_state, action, next_state)
                    + delta * _policy_evaluation(policy, states, depth - 1)[next_state]
                )

        return values
