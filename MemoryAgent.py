class MemoryAgent:
    # Same idea as BaselineAgent (go to the nearest unvisited city),
    # but it remembers failed trips and treats those roads as more expensive.

    def __init__(self):
        # memory about roads: road -> how many times we tried it / how many times it failed
        self.attempts = {}
        self.fails = {}
        # last move, so we know which road the last_success from percept belongs to
        self.last_from = None
        self.last_to = None
        self.distance_matrix = None

    def act(self, percept):
        self.distance_matrix = percept.dist_matrix
        current_city = percept.current_city

        # Remember the result of the previous move
        if self.last_to is not None:
            road = self._road(self.last_from, self.last_to)
            self.attempts[road] = self.attempts.get(road, 0) + 1
            if not percept.last_success:
                self.fails[road] = self.fails.get(road, 0) + 1

        # All cities visited, go to the base
        if len(percept.visited) == len(percept.cities):
            target = 0
        else:
            # the cheapest unvisited city, cost includes what we learned about the road
            cost_temp = float("inf")
            for i in range(len(percept.cities)):
                if i not in percept.visited and self._cost(current_city, i) < cost_temp:
                    cost_temp = self._cost(current_city, i)
                    target = i

        self.last_from = current_city
        self.last_to = target
        return target

    def _road(self, a, b):
        # same key for a->b and b->a: the smaller city always goes first
        if a < b:
            return (a, b)
        else:
            return (b, a)

    def _cost(self, a, b):
        # Expected cost of the road. If the road failed before, it is more expensive for us.
        # p - estimated chance of failure, 1 / (1 - p) - expected number of tries
        road = self._road(a, b)
        attempts = self.attempts.get(road, 0)
        fails = self.fails.get(road, 0)
        p = fails / (attempts + 1)
        return self.distance_matrix[a][b] / (1 - p)
