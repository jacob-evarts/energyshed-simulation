from Agents.Household import Household


class GridHousehold(Household):
    def setup(self):
        """Initialize a new variable at agent creation."""
        super().setup()

    def update_energy(self, sunny):
        super().update_energy(sunny)

    def energy_decision(self):
        if self.energy_bal < 0:
            self.action = "buy"
            self.status = -1
        elif self.energy_bal > 0:
            self.action = "sell"
            self.status = 1

    def buy(self):
        # Need to buy energy
        if self.action == "buy":
            self._buy_energy()

    def store(self):
        pass

    def sell(self):
        if self.action == "sell":
            self.daily_cost += self.energy_bal
            self.total_cost += self.daily_cost

    def _buy_energy(self):
        # Buy from the grid
        # Transfer
        transfered = abs(self.energy_bal)
        self.grid_trans += transfered
        # Balance
        self.energy_bal = 0
        # Cost
        self.daily_cost += -(transfered * 10)
        self.total_cost += self.daily_cost
