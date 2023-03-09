from node_queue import NodeQueue
from Agents.Household import Household


class ReflexHousehold(Household):
    def buy(self):
        # Need to buy energy
        if self.action == "buy":
            self._buy_energy()

    def store(self):
        pass

    def sell(self):
        pass

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
                seller.daily_cost += transfered
                seller.total_cost += seller.daily_cost
                self.daily_cost += -(transfered * distance)
                self.total_cost += self.daily_cost

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
                seller.daily_cost += transfered
                seller.total_cost += seller.daily_cost
                self.daily_cost = -(transfered * distance)
                self.total_cost += self.daily_cost

        # Buy from the grid
        else:
            # Transfer
            transfered = abs(self.energy_bal)
            self.grid_trans += transfered
            # Balance
            self.energy_bal = 0
            # Cost
            self.daily_cost += -(transfered * 10)
            self.total_cost += self.daily_cost

    def _bfs(self):
        queue = NodeQueue()
        queue.enqueue(self)
        distances = {self: 0}
        while not queue.is_empty():
            parent_node = queue.dequeue()
            for child in self.network.neighbors(parent_node):
                # If the node is a seller, return it
                if child.action == "sell" and child.energy_bal > 0:
                    return child, (distances[parent_node] + 1)
                if child not in distances:
                    distances[child] = distances[parent_node] + 1
                    queue.enqueue(child)
        return None, None


class ReflexSellHousehold(ReflexHousehold):
    def energy_decision(self):
        if self.energy_bal < 0:
            self.action = "buy"
            self.status = -1
        elif self.energy_bal >= 0:
            self.action = "sell"
            self.status = 1

    def sell(self):
        if self.action == "sell":
            self.daily_cost += self.energy_bal
            self.total_cost += self.daily_cost


class ReflexStoreHousehold(ReflexHousehold):
    def setup(self):
        """Initialize a new variable at agent creation."""
        super().setup()
        self.storage = 0

    def energy_decision(self):
        # Use stored energy if available
        if self.storage > 0:
            self.energy_bal += self.storage
            self.storage = 0

        if self.energy_bal < 0:
            self.action = "buy"
            self.status = -1
        elif self.energy_bal >= 0:
            self.action = "store"
            self.status = 0

    def store(self):
        if self.action == "store":
            transfered = self.energy_bal
            self.storage += transfered
            self.energy_bal = 0
