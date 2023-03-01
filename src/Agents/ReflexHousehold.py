from node_queue import NodeQueue
from Agents.Household import Household


class ReflexHousehold(Household):
    def setup(self):
        """Initialize a new variable at agent creation."""
        super().setup()

    def update_energy(self, sunny):
        super().update_energy(sunny)

    def set_status(self):
        super().set_status()

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
                transfered = abs(seller.energy_bal)
                self.local_trans += transfered
                # Balance
                self.energy_bal = self.energy_bal + seller.energy_bal
                seller.energy_bal = 0
                # Cost
                seller.cost += transfered
                self.cost -= transfered * distance

                if self.energy_bal < 0:
                    self._buy_energy()

            # Buy some of neighbor's energy
            elif abs(self.energy_bal) < seller.energy_bal:
                # Transfer
                transfered = abs(self.energy_bal)
                self.local_trans += transfered
                # Balance
                seller.energy_bal = seller.energy_bal + self.energy_bal
                self.energy_bal = 0
                # Cost
                seller.cost += transfered
                self.cost -= transfered * distance

        # Buy from the grid
        else:
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

    def _bfs(self):
        queue = NodeQueue()
        queue.enqueue(self)
        distances = {self: 0}
        while not queue.is_empty():
            parent_node = queue.dequeue()
            for child in self.network.neighbors(parent_node):
                # If the node is a seller, return it
                if child.energy_bal > 0:
                    return child, distances[parent_node] + 1
                if child not in distances:
                    distances[child] = distances[parent_node] + 1
                    queue.enqueue(child)
        return None, None
