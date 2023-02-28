import random
import agentpy as ap


class Household(ap.Agent):
    def setup(self):
        self.status = 0
        self.production = 10
        self.consumption = 10
        self.energy_bal = self.production - self.consumption

        self.local_trans = 0
        self.grid_trans = 0
        self.cost = 0

    def update_energy(self, sunny):
        # Account for variability in production and consumption (shading, wind, temperature)
        if sunny:
            self.production = random.normalvariate(10, 2)
        else:
            self.production = random.normalvariate(8, 2)

        self.energy_bal = self.production - self.consumption

    def set_status(self):
        # Excess of energy
        if self.energy_bal > 0:
            self.status = 1
        # Need to buy energy
        elif self.energy_bal < 0:
            self.status = -1
        else:
            self.status = 0

    def energy_decision(self):
        raise NotImplementedError

    def _buy_energy(self):
        raise NotImplementedError

    def sell_remaining(self):
        raise NotImplementedError
