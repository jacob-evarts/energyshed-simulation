from Agents.Household import Household


class GridHousehold(Household):
    def setup(self):
        """Initialize a new variable at agent creation."""
        super().setup()

    def update_energy(self, sunny):
        super().update_energy(sunny)

    def set_status(self):
        super().set_status()

    def energy_decision(self):
        # Need to buy energy
        if self.status == -1:
            self._buy_energy()

    def _buy_energy(self):
        # Buy from the grid
        # Transfer
        transfered = abs(self.energy_bal)
        self.grid_trans += transfered
        # Balance
        self.energy_bal = 0
        # Cost
        self.cost -= transfered * 10

    def sell_remaining(self):
        if self.energy_bal > 0:
            self.energy_bal = 0
            self.cost += self.energy_bal
