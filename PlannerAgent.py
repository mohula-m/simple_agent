class PlannerAgent:
    def __init__(self):
        self.attemts = {}
        self.fails = {}
        self.last_from = None
        self.last_to = None
        self.distance_matrix = None

    def act(self, percept):
        self.distance_matrix = percept.dist_matrix
        unvisited = []
        for city in range(len(percept.cities)):
            if city not in percept.visited:
                unvisited.append(city)
        # All cities visited, go to the base
        if len(unvisited) == 0:
            return 0

        route = self._greedy_route(percept.current_city, unvisited)

        # Improve
        route = self._two_opt(route)

        # Where we are, route[1] - where to go now
        return route[1]

    def _greedy_route(self, start, cities_to_visit):
        route = [start]
        remaining = list(cities_to_visit)

        while len(remaining) > 0:
            last = route[-1]

            # find the city nearest to the last city of the route
            nearest = remaining[0]
            for city in remaining:
                if self.distance_matrix[last][city] < self.distance_matrix[last][nearest]:
                    nearest = city

            route.append(nearest)
            remaining.remove(nearest)

        route.append(0)
        return route

    def _two_opt(self, route):
        # Improves the route: reverses parts of it if that makes the route shorter.
        # The first city (where we are) and the last one (base) are never moved.
        d = self.distance_matrix
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

                    old_length = d[a][b] + d[c][e]
                    new_length = d[a][c] + d[b][e]

                    # small margin prevents an infinite loop caused by float rounding errors
                    if new_length < old_length - 1e-9:
                        route[i:j + 1] = route[i:j + 1][::-1]
                        improved = True

        return route
