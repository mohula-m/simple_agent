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

        # состояние эпизода
        self.base = 0                     # индекс базы (старт и финиш)
        self.current = self.base          # где сейчас курьер
        self.visited = {self.base}        # посещённые города
        self.total_cost = 0.0             # сколько потрачено, включая проваленные поездки
        self.steps = 0                    # сколько сделано ходов
        self.failures = 0                 # сколько поездок провалилось
        self.last_success = True          # удалась ли последняя поездка

    def _generate_bad_routes(self):
        # все дороги: пары (i, j), где i < j, чтобы 2->7 и 7->2 были одной дорогой
        all_routes = []
        for i in range(self.cities_count):
            for j in range(i + 1, self.cities_count):
                all_routes.append((i, j))

        bad_count = round(self.bad_ratio * len(all_routes))
        return set(self.rng.sample(all_routes, bad_count))


    def step(self, target_city_index):
        # Актуатор: агент просит поехать в target_city_index, среда решает, что произошло.
        # Возвращает True, если курьер доехал, и False, если поездка провалилась.

        # 1. Проверки: среда не доверяет агенту и сама следит за правилами мира
        if not (0 <= target_city_index < self.cities_count):
            raise ValueError(f"Города {target_city_index} не существует (всего {self.cities_count})")
        if target_city_index == self.current:
            raise ValueError(f"Курьер уже находится в городе {target_city_index}")

        # 2. Поездка стоит денег/времени всегда, даже если окончится провалом
        self.steps += 1
        self.total_cost += self.dist_matrix[self.current][target_city_index]

        # 3. Провал возможен только на плохой дороге и только с вероятностью fail_prob
        if self.is_bad_route(self.current, target_city_index) and self.rng.random() < self.fail_prob:
            # курьер не проехал и остаётся на месте
            self.failures += 1
            self.last_success = False
        else:
            # курьер доехал: переезжает и отмечает город как посещённый
            self.current = target_city_index
            self.visited.add(target_city_index)
            self.last_success = True

        return self.last_success

    def get_percept(self):
        # Сенсор: снимок того, что агенту разрешено знать в данный момент.
        # Отдаём копии (tuple, frozenset), чтобы агент не мог изменить состояние среды.
        return Percept(
            current_city=self.current,
            cities=tuple(self.cities),
            visited=frozenset(self.visited),
            last_success=self.last_success,
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
        # Эпизод закончен, когда посещены все города и курьер вернулся на базу
        return len(self.visited) == self.cities_count and self.current == self.base