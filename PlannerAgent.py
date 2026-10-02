class PlannerAgent:
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

        # Remember the result of the previous move
        if self.last_to is not None:
            road = self._road(self.last_from, self.last_to)
            self.attempts[road] = self.attempts.get(road, 0) + 1
            if not percept.last_success:
                self.fails[road] = self.fails.get(road, 0) + 1

        unvisited = []
        for city in range(len(percept.cities)):
            if city not in percept.visited:
                unvisited.append(city)

        # All cities visited, go to the base
        if len(unvisited) == 0:
            target = 0
        else:
            route = self._greedy_route(percept.current_city, unvisited)

            # Improve
            route = self._two_opt(route)

            # Where we are, route[1] - where to go now
            target = route[1]

        self.last_from = percept.current_city
        self.last_to = target
        return target

    def _road(self, a, b):
        # same key for a->b and b->a
        return (min(a, b), max(a, b))

    def _cost(self, a, b):
        # Expected cost of the road. If the road failed before, it is more expensive for us.
        # p - estimated chance of failure, 1 / (1 - p) - expected number of tries
        road = self._road(a, b)
        attempts = self.attempts.get(road, 0)
        fails = self.fails.get(road, 0)
        p = fails / (attempts + 1)
        return self.distance_matrix[a][b] / (1 - p)

    def _greedy_route(self, start, cities_to_visit):
        route = [start]
        remaining = list(cities_to_visit)

        while len(remaining) > 0:
            last = route[-1]

            # find the city nearest to the last city of the route
            nearest = remaining[0]
            for city in remaining:
                if self._cost(last, city) < self._cost(last, nearest):
                    nearest = city

            route.append(nearest)
            remaining.remove(nearest)

        route.append(0)
        return route

    def _two_opt(self, route):
        # Improves the route: reverses parts of it if that makes the route shorter.
        # The first city (where we are) and the last one (base) are never moved.
        improved = True

        while improved:
            improved = False

            for i in range(1, len(route) - 2):
                for j in range(i + 1, len(route) - 1):
                    # Reversing route changes only the two routes

                    a = route[i - 1]
                    b = route[i]
                    c = route[j]
                    e = route[j + 1]

                    old_length = self._cost(a, b) + self._cost(c, e)
                    new_length = self._cost(a, c) + self._cost(b, e)

                    # small margin prevents an infinite loop caused by float rounding errors
                    if new_length < old_length - 1e-9:
                        route[i:j + 1] = route[i:j + 1][::-1]
                        improved = True

        return route
