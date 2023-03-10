import random
import agentpy as ap

random.seed(42)


class Household(ap.Agent):
    def setup(self):
        self.action = None
        self.status = 0
        self.producer = random.random() < self.model.percent_producers
        if self.producer:
            self.production = random.normalvariate(10, 2)
        else:
            self.production = 0
        self.consumption = 10
        self.energy_bal = self.production - self.consumption

        self.local_trans = 0
        self.grid_trans = 0
        self.daily_cost = 0
        self.total_cost = 0

    def update_energy(self, weather):
        # Account for variability in production (shading, wind, temperature)
        if self.producer:
            if weather == "sun":
                self.production = random.normalvariate(11, 2)
            else:
                self.production = random.normalvariate(7, 2)

        self.energy_bal = self.production - self.consumption

        self.grid_trans = 0
        self.local_trans = 0
        self.daily_cost = 0

    def energy_decision(self):
        raise NotImplementedError

    def buy(self):
        raise NotImplementedError

    def store(self):
        raise NotImplementedError

    def sell(self):
        raise NotImplementedError
