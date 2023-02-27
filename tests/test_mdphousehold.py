import unittest
import random
from demo.MDPHousehold import MDPHousehold


class TestMDPHousehold(unittest.TestCase):
    def test_policy_evaluation(self):
        states = [
            (1, "sunny"),
            (0, "sunny"),
            (-1, "sunny"),
            (1, "cloudy"),
            (0, "cloudy"),
            (-1, "cloudy"),
        ]
        actions = ["buy", "sell", "none"]
        delta = 0.9
        depth = 3
        policy = {state: random.choice(actions) for state in states}
        print(policy)
        print(agent._policy_evaluation(policy, states, delta, depth))


if __name__ == "__main__":
    unittest.main()
