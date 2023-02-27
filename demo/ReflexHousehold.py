import random
import agentpy as ap

from node_queue import NodeQueue


class ReflexHousehold(ap.Agent):
    def setup(self):
        """Initialize a new variable at agent creation."""
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
            self.production = random.normalvariate(9, 2)
        else:
            self.production = random.normalvariate(7, 2)

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
        # Need to buy energy
        if self.energy_bal < 0:
            self._buy_energy()

    def _buy_energy(self):
        seller, distance = self._bfs()
        if seller:
            # Buy all of neighbor's energy
            if abs(self.energy_bal) >= seller.energy_bal:
                # Transfer
                self.local_trans += abs(seller.energy_bal)
                # Balance
                self.energy_bal = self.energy_bal + seller.energy_bal
                seller.energy_bal = 0
                seller.status = 0
                # Cost
                seller.cost += seller.local_trans
                self.cost -= seller.local_trans * distance

                if self.energy_bal < 0:
                    self._buy_energy()

            # Buy some of neighbor's energy
            elif abs(self.energy_bal) < seller.energy_bal:
                # Transfer
                self.local_trans += abs(self.energy_bal)
                # Balance
                seller.energy_bal = seller.energy_bal + self.energy_bal
                self.energy_bal = 0
                self.status = 0
                # Cost
                seller.cost += seller.local_trans
                self.cost -= seller.local_trans * distance

        # Buy from the grid
        else:
            # Trnasfer
            self.grid_trans += self.energy_bal
            # Balance
            self.energy_bal = 0
            # Cost
            self.cost -= self.energy_bal * 5

    def _bfs(self):
        queue = NodeQueue()
        queue.enqueue(self)
        distances = {self: 0}
        while not queue.is_empty():
            parent_node = queue.dequeue()
            for child in self.network.neighbors(parent_node):
                # If the node is a seller, return it
                if child.status == 1:
                    return child, distances[parent_node] + 1
                if child not in distances:
                    distances[child] = distances[parent_node] + 1
                    queue.enqueue(child)
        return None, None
