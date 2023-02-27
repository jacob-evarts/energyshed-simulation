import random
import agentpy as ap
import networkx as nx

from ReflexHousehold import ReflexHousehold

SUN_PROBABILITY = 0.5


class EnergyShedModel(ap.Model):
    def setup(self):
        """Initialize the agents and network of the model."""
        # Initialize weather
        self.sunny = True if random.random() < SUN_PROBABILITY else False

        self.status_map = {-1: "buy", 0: "none", 1: "sell"}
        # Create agents
        self.agents = ap.AgentDList(self, self.p.population, ReflexHousehold)

        # Prepare a small-world network
        # graph = nx.watts_strogatz_graph(
        #     self.p.population, self.p.number_of_neighbors, self.p.network_randomness
        # )
        # self.network = self.agents.network = ap.Network(self, graph)
        # self.network.add_agents(self.agents, self.graph.nodes)

        # Prepare a grid
        self.network = self.agents.network = ap.Grid(self, self.p.grid_size)
        self.network.add_agents(self.agents, random=True)

    def update(self):
        """Record variables after setup and each step."""
        # Model level recording
        for i, state in enumerate((0, -1, 1)):
            n_agents = len(self.agents.select(self.agents.status == state))
            self[self.status_map[state]] = n_agents / self.p.population
            self.record(self.status_map[state])

        self["energy_production"] = sum(self.agents.production)
        self.record("energy_production")
        self["energy_transfer"] = sum(self.agents.energy_trans)
        self.record("energy_transfer")
        self["weather"] = "Sunny" if self.sunny else "Cloudy"
        self.record("weather")

        # Agent level recording
        self.agents.record("production")
        self.agents.record("consumption")
        self.agents.record("energy_bal")

    def step(self):
        """Define the models' events per simulation step."""
        # Update weather
        self.sunny = True if random.random() < SUN_PROBABILITY else False
        self.agents.update_energy(self.sunny)
        self.agents.energy_decision()

    def end(self):
        """Record evaluation measures at the end of the simulation."""
        # Record final evaluation measures
        self.report("Per household energy transfer", self.agents.energy_trans)
        self.report("Peak energy production", max(self.log["energy_production"]))
        self.report("Total Energy Production", sum(self.log["energy_production"]))
        self.report("Total Energy Transfer", sum(self.log["energy_transfer"]))

    def get_cost(self):
        """Return the cost of the energy transfer."""
        return sum(self.agents.energy_trans)

    def get_weather(self):
        """Return the weather of the current step."""
        return "sunny" if self.sunny else "cloudy"
