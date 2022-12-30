import agentpy as ap
import random

class Household(ap.Agent):
    def setup(self):
        """Initialize a new variable at agent creation."""
        self.condition = 0  # Susceptible/None = 0, Infected/Buy = 1, Recovered/Sell = 2, Store = 3
        self.production = random.randrange(
            0, 10, 1
        )  # (start,stop, step) + random.random() # float part
        self.consumption = random.randrange(1, 10, 1)  # + random.random() # float part
        self.storage_cap = random.randrange(0, 10, 1)  # + random.random() # float part
        self.energy_bal = self.production - self.consumption
        self.storage_util = 0
        self.energy_trans = 0
        self.flag = "init"
        self.color = "blue"

    def energy_decision(self):
        # print(self.energy_bal)
        if self.energy_bal > 0:
            # sell energy to neighbor who wants to buy it OR STORE - set flag to store
            self.flag = "sell"  # or make this 0, 1, 2 for nothing, buy, sell???
            self.color = "green"
            for n in self.network.neighbors(self):  # define distance, determine # hops
                if n.energy_bal < 0 and n.flag == "buy":
                    if self.energy_bal > abs(n.energy_bal):  # my bal > abs(neighbor)
                        self.energy_bal = self.energy_bal + n.energy_bal
                        self.energy_trans = abs(n.energy_bal)  # track energy transferred
                        n.energy_bal = 0
                        n.flag = "bal"
                        self.condition = 2
                        n.condition = 1

                    elif self.energy_bal < abs(
                        n.energy_bal
                    ):  # neighbor needs more than I have, sell all to neighbor
                        n.energy_bal = n.energy_bal + self.energy_bal
                        self.energy_trans = (
                            self.energy_bal
                        )  # xfer entire bl - track energy transferred
                        self.energy_bal = 0
                        self.flag = "bal"
                        self.condition = 2
                        n.condition = 1
                # Or use battery and store excess energy based on price TBD

        elif self.energy_bal < 0:
            # buy energy from neighbor
            # define distance, determine # hops 2 loops check 1-hop neighbors, check 2-hop, check n-hop neighbors
            self.flag = "buy"
            self.color = "yellow"
            for n in self.network.neighbors(self):
                if n.energy_bal > 0 and n.flag == "sell":
                    if abs(self.energy_bal) > n.energy_bal:
                        self.energy_bal = self.energy_bal + n.energy_bal
                        n.energy_trans = (
                            n.energy_bal
                        )  # buy all neighbor energy - track energy transferred
                        n.energy_bal = 0
                        n.flag = "bal"
                        self.condition = 1
                        n.condition = 2

                    elif abs(self.energy_bal) < n.energy_bal:  # buy some of neighbor's energy
                        n.energy_bal = (
                            n.energy_bal + self.energy_bal
                        )  # add self neg bal to neigh pos bal
                        n.energy_trans = abs(
                            self.energy_bal
                        )  # self bal is xfered - track energy transferred
                        self.energy_bal = 0  # set self bal = 0
                        self.flag = "bal"
                        self.condition = 1
                        n.condition = 2

        elif self.energy_bal == 0:
            # do nothing
            self.condition = 0

        if self.energy_bal > 0 and self.storage_util < self.storage_cap:
            self.storage_util = self.storage_util + self.energy_bal
            if self.storage_util > self.storage_cap:
                self.storage_util = self.storage_cap
                self.color = "dark green"
                self.condition = 3

        ## version 2 we will select from a group of neighbors the lowest selling price/highest buying price
        ## at end of turn if excess energy in system - add to storage or delete (send back to grid at defalult price)

    def update_energy(self):
        # rng = self.model.random
        # rng = random.randrange(10) + random.random()

        # Account for variability in production (shading, wind)
        self.production = self.production * round(random.triangular(0.4, 1), 1)
        if self.production > 0:
            self.flag = "sell"
            self.color = "green"
            self.condition = (
                2  # Susceptible/None = 0, Infected/Buy = 1, Recovered/Sell = 2, Store = 3
            )

        # add randomness to consumption
        self.consumption = self.consumption * round(random.triangular(0.4, 1.5), 1)
        if self.consumption > self.production:  # and self.storage_util == 0:
            self.flag = "buy"
            self.color = "yellow"
            self.condition = (
                1  # Susceptible/None = 0, Infected/Buy = 1, Recovered/Sell = 2, Store = 3
            )

        # set flags, colors

    # def being_sick(self):
    #    """ Spread disease to peers in the network. """
    #    rng = self.model.random
    #    for n in self.network.neighbors(self):
    #        if n.condition == 0 and self.p.infection_chance > rng.random():
    #            n.condition = 1  # Infect susceptible peer
    #    if self.p.recovery_chance > rng.random():
    #        self.condition = 2  # Recover from infection