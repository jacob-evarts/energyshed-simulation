import random
import agentpy as ap
import networkx as nx
import logging

from Agents.GridHousehold import GridHousehold
from Agents.ReflexHousehold import ReflexSellHousehold, ReflexStoreHousehold
from Agents.QHousehold import QHousehold


class EnergyShedModel(ap.Model):
    def setup(self):
        """Initialize the agents and network of the model."""
        # Logging
        logging.basicConfig(
            filename=f"logs/{self.p.agent_type}_simulation.log", level=logging.INFO, force=True
        )

        # Initialize weather
        self.sun_prob = self.p.sunny_prob
        self.forcast = [
            "sun" if random.random() < self.sun_prob else "clouds" for _ in range(self.p.steps)
        ]
        self.weather = self.forcast[0]

        # Create agents
        self.percent_producers = self.p.percent_producers
        if self.p.agent_type == "grid":
            self.agents = ap.AgentList(self, self.p.population, GridHousehold)
        elif self.p.agent_type == "reflex_sell":
            self.agents = ap.AgentList(self, self.p.population, ReflexSellHousehold)
        elif self.p.agent_type == "reflex_store":
            self.agents = ap.AgentList(self, self.p.population, ReflexStoreHousehold)
        elif self.p.agent_type == "qlearning":
            self.agents = ap.AgentList(self, self.p.population, QHousehold)

        # Initialize a network
        self.network = self.agents.network = ap.Grid(self, self.p.grid_size, check_border=False)
        self.network.add_agents(self.agents)

    def update(self):
        """Record variables after setup and each step."""
        # Model level recording
        for i, state in enumerate(("sell", "buy", "store")):
            n_agents = len(self.agents.select(self.agents.action == state))
            self[state] = n_agents / self.p.population
            self.record(state)

        self["energy_production"] = sum(self.agents.production)
        self.record("energy_production")

        self["local_transfer"] = sum(self.agents.local_trans)
        self.record("local_transfer")
        self["grid_transfer"] = sum(self.agents.grid_trans)
        self.record("grid_transfer")

        self["daily_cost"] = sum(self.agents.daily_cost) / self.p.population
        self.record("daily_cost")

        self["weather"] = self.weather
        self.record("weather")
        # Record qlearner specific values
        if self.p.agent_type == "qlearning":
            q_values = self.agents[0].get_q_values()
            self["q_values"] = q_values
            self.record("q_values")
            self["reward"] = sum(self.agents.get_reward()) / self.p.population
            self.record("reward")

        # Agent level recording
        self.agents.record("action")
        self.agents.record("production")
        self.agents.record("consumption")
        self.agents.record("energy_bal")
        self.agents.record("daily_cost")
        self.agents.record("local_trans")
        self.agents.record("grid_trans")

    def step(self):
        """Define the models' events per simulation step."""
        # Update weather
        if self.t != 1:
            self.weather = self.forcast[self.t - 1]
        if self.t < self.p.steps:
            weather_tomorrow = self.forcast[self.t]
        else:
            weather_tomorrow = "clouds"

        # Log information from one particular agent
        tracked_agent = self.agents[0]
        self.agents.update_energy(self.weather)
        self.agents.energy_decision()
        self.agents.buy()
        self.agents.store()
        self.agents.sell()

        if self.p.agent_type == "qlearning":
            self.agents.update_q_values(weather_tomorrow)

        self.log_agent(logging, tracked_agent)

    def end(self):
        """Record evaluation measures at the end of the simulation."""
        # Record final evaluation measures
        self.report("Per household local energy transfer", self.agents.local_trans)
        self.report("Per household grid energy transfer", self.agents.grid_trans)
        self.report("Peak energy production", max(self.log["energy_production"]))
        self.report("Total Energy Production", sum(self.log["energy_production"]))
        self.report("Total local Transfer", sum(self.log["local_transfer"]))
        self.report("Total grid Transfer", sum(self.log["grid_transfer"]))
        self.report("Number of producers", len(self.agents.select(self.agents.producer)))
        self.report("Total Cost", sum(self.agents.total_cost))

    def log_agent(self, logging, tracked_agent):
        logging.info(f"-- Step {self.t} --")
        if self.p.agent_type == "qlearning":
            q_val = tracked_agent.get_q_value(tracked_agent.current_state, tracked_agent.action)
            logging.info(f"Current state: {tracked_agent.current_state}")
            logging.info(f"Action: {tracked_agent.action}")
            logging.info(
                f"Q-value <- (1 - lr) * Q_value + lr * (reward + discount * max(Q-value-next))"
            )
            logging.info(
                f"Q-value <- (1 - {tracked_agent.learning_rate}) * {q_val} + {tracked_agent.learning_rate} * ({tracked_agent.get_reward()} + {tracked_agent.discount_factor} * max(Q-value-next)))"
            )
            logging.info(f"Q-value: {q_val}")
            logging.info(f"Reward: {tracked_agent.get_reward()}")

        logging.info(
            f"Grid transfered: {tracked_agent.grid_trans}, Local transferred: {tracked_agent.local_trans}"
        )
        logging.info(
            f"Energy balance: {tracked_agent.energy_bal}, Daily cost: {tracked_agent.daily_cost}"
        )
