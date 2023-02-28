import random
import agentpy as ap
import networkx as nx

from Agents.GridHousehold import GridHousehold
from Agents.ReflexHousehold import ReflexHousehold
from Agents.MDPHousehold import MDPHousehold


SUN_PROBABILITY = 0.5


class EnergyShedModel(ap.Model):
    def setup(self):
        """Initialize the agents and network of the model."""
        # Initialize weather
        self.sunny = True if random.random() < SUN_PROBABILITY else False

        # Create agents
        if self.p.agent_type == "grid":
            self.agents = ap.AgentDList(self, self.p.population, GridHousehold)
        elif self.p.agent_type == "reflex":
            self.agents = ap.AgentDList(self, self.p.population, ReflexHousehold)
        elif self.p.agent_type == "mdp":
            self.agents.ap.AgentDlist(self, self.p.population, MDPHousehold)

        # Initialize a network
        self.network = self.agents.network = ap.Grid(self, self.p.grid_size)
        self.network.add_agents(self.agents)

        self.status_map = {-1: "buy", 0: "none", 1: "sell"}

    def update(self):
        """Record variables after setup and each step."""
        # Model level recording
        for i, state in enumerate((0, -1, 1)):
            n_agents = len(self.agents.select(self.agents.status == state))
            self[self.status_map[state]] = n_agents / self.p.population
            self.record(self.status_map[state])

        self["energy_production"] = sum(self.agents.production)
        self.record("energy_production")
        self["local_transfer"] = sum(self.agents.local_trans)
        self.record("local_transfer")
        self["grid_transfer"] = sum(self.agents.grid_trans)
        self.record("grid_transfer")
        self["cost"] = sum(self.agents.cost)
        self.record("cost")
        self["weather"] = "Sunny" if self.sunny else "Cloudy"
        self.record("weather")

        # Agent level recording
        self.agents.record("production")
        self.agents.record("consumption")
        self.agents.record("energy_bal")
        self.agents.record("cost")

    def step(self):
        """Define the models' events per simulation step."""
        # Update weather
        self.sunny = True if random.random() < SUN_PROBABILITY else False

        self.agents.update_energy(self.sunny)
        self.agents.set_status()
        self.agents.energy_decision()
        self.agents.sell_remaining()

    def end(self):
        """Record evaluation measures at the end of the simulation."""
        # Record final evaluation measures
        self.report("Per household local energy transfer", self.agents.local_trans)
        self.report("Per household grid energy transfer", self.agents.grid_trans)
        self.report("Peak energy production", max(self.log["energy_production"]))
        self.report("Total Energy Production", sum(self.log["energy_production"]))
        self.report("Total local Transfer", sum(self.log["local_transfer"]))
        self.report("Total grid Transfer", sum(self.log["grid_transfer"]))
        self.report("Total Cost", sum(self.agents.cost))

    def get_cost(self):
        """Return the cost of the energy transfer."""
        return sum(self.agents.cost)

    def get_weather(self):
        """Return the weather of the current step."""
        return "sunny" if self.sunny else "cloudy"
