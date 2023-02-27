import random
import agentpy as ap


class ReflexHousehold(ap.Agent):
    def setup(self):
        """Initialize a new variable at agent creation."""
        self.status = 0
        self.production = 10
        self.consumption = 10
        self.energy_bal = self.production - self.consumption

        self.energy_trans = 0

    def energy_decision(self):
        # Excess of energy
        if self.energy_bal > 0:
            self.status = 1
            self._sell_energy()
        # Need to buy energy
        elif self.energy_bal < 0:
            self.status = -1
            self._buy_energy()
        else:
            self.status = 0

    def update_energy(self, sunny):
        # Account for variability in production and consumption (shading, wind, temperature)
        if sunny:
            self.production = random.normalvariate(11, 2)
        else:
            self.production = random.normalvariate(9, 2)

        self.energy_bal = self.production - self.consumption

    def _sell_energy(self):
        # sell energy to neighbor who wants to buy it
        for n in self.network.neighbors(self):
            # Assume you only have information about the neighbors flag
            if n.status == -1:
                # sell them all they need
                if self.energy_bal >= abs(n.energy_bal):
                    self.energy_bal = self.energy_bal + n.energy_bal
                    self.energy_trans = abs(n.energy_bal)
                    n.energy_bal = 0
                    n.status = 0
                    if self.energy_bal == 0:
                        break

                # sell them all I have
                elif self.energy_bal < abs(n.energy_bal):
                    n.energy_bal = n.energy_bal + self.energy_bal
                    self.energy_trans = self.energy_bal
                    self.energy_bal = 0
                    self.status = 0

    def _buy_energy(self):
        # cheapest_price = float('inf')
        # cheapest_neighbor = None
        # for

        # buy energy from neighbor
        for n in self.network.neighbors(self):
            if n.status == 1:
                # buy all energy neighbor has
                if abs(self.energy_bal) >= n.energy_bal:
                    self.energy_bal = self.energy_bal + n.energy_bal
                    # buy all neighbor energy - track energy transferred
                    n.energy_trans = n.energy_bal
                    n.energy_bal = 0
                    n.status = 0
                    if self.energy_bal == 0:
                        break

                # buy some of neighbor's energy
                elif abs(self.energy_bal) < n.energy_bal:
                    n.energy_bal = n.energy_bal + self.energy_bal
                    # self bal is xfered - track energy transferred
                    n.energy_trans = abs(self.energy_bal)
                    self.energy_bal = 0
                    self.status = 0
