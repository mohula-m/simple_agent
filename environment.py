import random
import math
import numpy as np
from city import City
from percept import Percept

CITIES_NAMES = [
    "Bratislava",
    "Petrzalka",
    "Senec",
    "Pezinok",
    "Modra",
    "Stupava",
    "Malacky",
    "Svaty Jur",
    "Bernolakovo",
    "Ivanka pri Dunaji",
    "Dunajska Luzna",
    "Rusovce",
    "Cunovo",
    "Jarovce",
    "Chorvatsky Grob",
    "Slovensky Grob",
    "Trnava",
    "Sered",
    "Galanta",
    "Dunajska Streda",
    "Samorin",
    "Sturovo",
    "Hainburg",
    "Wolfsthal",
    "Kittsee",
    "Bruck an der Leitha",
    "Schwechat",
    "Wien",
    "Mosonmagyarovar",
    "Rajka",
]


def distance(a, b):
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)


class Environment:
    def __init__(self, map_size, cities_count, seed, bad_ratio, fail_prob):
        self.map_size = map_size
        self.rng = random.Random(seed)
        self.cities_count = cities_count
        self.bad_ratio = bad_ratio
        self.cities = self._generate_cities()
        self.dist_matrix = self._build_dist_matrix()
        self.bad_routes = self._generate_bad_routes()
        self.fail_prob = fail_prob

        # episode state
        self.base = 0                     # base index (start and finish)
        self.current = self.base          # where the courier is now
        self.visited = {self.base}        # visited cities
        self.total_cost = 0.0             # total cost, including failed trips
        self.steps = 0                    # number of moves made
        self.failures = 0                 # number of failed trips
        self.last_success = True          # whether the last trip succeeded

    def _generate_bad_routes(self):
        # all roads: pairs (i, j) with i < j, so 2->7 and 7->2 are the same road
        all_routes = []
        for i in range(self.cities_count):
            for j in range(i + 1, self.cities_count):
                all_routes.append((i, j))

        bad_count = round(self.bad_ratio * len(all_routes))
        return set(self.rng.sample(all_routes, bad_count))


    def step(self, target_city_index):
        # Actuator: the agent asks to go to target_city_index, the environment decides what happens.
        # Returns True if the courier arrived and False if the trip failed.

        # 1. Checks: the environment does not trust the agent and enforces the world rules itself
        if not (0 <= target_city_index < self.cities_count):
            raise ValueError(f"City {target_city_index} does not exist (total {self.cities_count})")
        if target_city_index == self.current:
            raise ValueError(f"Courier is already in city {target_city_index}")

        # 2. A trip always costs money/time, even if it fails
        self.steps += 1
        self.total_cost += self.dist_matrix[self.current][target_city_index]

        # 3. A failure is possible only on a bad road and only with probability fail_prob
        if self.is_bad_route(self.current, target_city_index) and self.rng.random() < self.fail_prob:
            # the courier did not get through and stays in place
            self.failures += 1
            self.last_success = False
        else:
            # the courier arrived: moves and marks the city as visited
            self.current = target_city_index
            self.visited.add(target_city_index)
            self.last_success = True

        return self.last_success

    def get_percept(self):
        # Sensor: a snapshot of what the agent is allowed to know at this moment.
        # Copies (tuple, frozenset) are given so the agent cannot change the environment state.
        return Percept(
            current_city=self.current,
            cities=tuple(self.cities),
            visited=frozenset(self.visited),
            last_success=self.last_success,
            dist_matrix=self.dist_matrix
        )

    def is_bad_route(self, a, b):
        return (min(a, b), max(a, b)) in self.bad_routes

    def _generate_cities(self):
        return [City(i, self.rng.randint(0, self.map_size), self.rng.randint(0, self.map_size), name)
                for i, name in enumerate(self.rng.sample(CITIES_NAMES, self.cities_count))]

    def _build_dist_matrix(self):
        dist_matrix = np.zeros((self.cities_count, self.cities_count))
        for i in range(self.cities_count):
            for j in range(self.cities_count):
                if i == j:
                    dist_matrix[i][j] = 0
                else:
                    dist_matrix[i][j] = distance(self.cities[i], self.cities[j])
        return dist_matrix

    def is_done(self):
        # The episode is over when all cities are visited and the courier is back at the base
        return len(self.visited) == self.cities_count and self.current == self.base