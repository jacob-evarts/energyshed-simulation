import agentpy as ap
import networkx as nx

from Household import Household

class EnergyShedModel(ap.Model):
    def setup(self):
        """Initialize the agents and network of the model."""

        # Prepare a small-world network
        graph = nx.watts_strogatz_graph(
            self.p.population, self.p.number_of_neighbors, self.p.network_randomness
        )

        # Create agents and network
        self.agents = ap.AgentList(self, self.p.population, Household)
        self.network = self.agents.network = ap.Network(self, graph)
        self.network.add_agents(self.agents, self.network.nodes)

        # Infect a random share of the population
        # I0 = int(self.p.initial_infection_share * self.p.population)
        # self.agents.random(I0).condition = 1

    def update(self):
        """Record variables after setup and each step."""

        # Record share of agents with each condition
        for i, c in enumerate(("None", "Buy", "Sell", "Store")):
            n_agents = len(self.agents.select(self.agents.condition == i))
            self[c] = n_agents / self.p.population
            self.record(c)

        self.record("Total Energy Balance", self.agents.energy_bal)
        self.record("Total Energy Transfer", self.agents.energy_trans)
        # tot_energy_xfer =

        # self.record('Gini Coefficient', gini(self.agents.wealth))
        # Stop simulation if disease is gone
        # if self.I == 0:
        #    self.stop()

    def step(self):
        """Define the models' events per simulation step."""

        # Call 'being_sick' for infected agents
        # self.agents.select(self.agents.condition == 1).being_sick()
        self.agents.energy_decision()
        self.agents.update_energy()
        # selling/buying/storing energy

    def get_tot_xfer(self):
        # Calculate average percentage of similar neighbors
        return sum(self.agents.energy_trans)

    def end(self):
        """Record evaluation measures at the end of the simulation."""

        # Record final evaluation measures
        # energy bal
        # storage capacity
        self.report("Per Agent energy transfer", self.agents.energy_trans)
        self.report("Total Energy Transfer", self.get_tot_xfer())

        # self.report('Peak share infected', max(self.log['I']))

    # def end(self):
    #    # Measure segregation at the end of the simulation
    #    self.report('segregation', self.get_segregation())