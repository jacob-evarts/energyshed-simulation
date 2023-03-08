import random
import agentpy as ap
import networkx as nx

from Agents.GridHousehold import GridHousehold
from Agents.ReflexHousehold import ReflexHousehold
from Agents.QHousehold import QHousehold


class EnergyShedModel(ap.Model):
    def setup(self):
        """Initialize the agents and network of the model."""
        # Initialize weather
        self.sun_prob = self.p.sunny_prob
        self.forcast = [
            True if random.random() < self.sun_prob else False for _ in range(self.p.steps)
        ]
        self.sunny = self.forcast[0]

        # Create agents
        self.percent_producers = self.p.percent_producers
        if self.p.agent_type == "grid":
            self.agents = ap.AgentDList(self, self.p.population, GridHousehold)
        elif self.p.agent_type == "reflex":
            self.agents = ap.AgentDList(self, self.p.population, ReflexHousehold)
        elif self.p.agent_type == "qlearning":
            self.agents = ap.AgentDList(self, self.p.population, QHousehold)

        # Initialize a network
        self.network = self.agents.network = ap.Grid(self, self.p.grid_size)
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

        self["daily_cost"] = sum(self.agents.daily_cost)
        self.record("daily_cost")

        self["weather"] = "sunny" if self.sunny else "cloudy"
        self.record("weather")

        # Agent level recording
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
            self.sunny = self.forcast[self.t - 1]
        if self.t < self.p.steps:
            sunny_tomorrow = self.forcast[self.t]
        else:
            sunny_tomorrow = False

        self.agents.update_energy(self.sunny)
        self.agents.energy_decision()
        self.agents.buy()
        self.agents.store()
        self.agents.sell()
        if self.p.agent_type == "qlearning":
            self.agents.update_q_values(sunny_tomorrow)
            tracked_agent = self.agents[0]
            print()
            # print(f"Q-values: {tracked_agent.q_values}")
            print(f"Current state: {tracked_agent.current_state}, Action: {tracked_agent.action}")
            print(
                f"Grid transfered: {tracked_agent.grid_trans}, Local transferred: {tracked_agent.local_trans}"
            )
            print(
                f"Energy balance: {tracked_agent.energy_bal}, Daily cost: {tracked_agent.daily_cost}"
            )
            print(f"Reward: {tracked_agent.get_reward()}")
            print()
        num_selling = 0
        num_buying = 0
        num_storing = 0
        for agent in self.agents:
            if agent.action == "sell":
                num_selling += 1
            elif agent.action == "buy":
                num_buying += 1
            elif agent.action == "store":
                num_storing += 1

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

    def get_cost(self):
        """Return the cost of the energy transfer."""
        return sum(self.agents.daily_cost)

    def get_weather(self):
        """Return the weather of the current step."""
        return "sunny" if self.sunny else "cloudy"
