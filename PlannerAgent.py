class PlannerAgent:
    def __init__(self):
        self.attemts = {}
        self.fails = {}
        self.last_from = None
        self.last_to = None
        self.distance_matrix = None

    def act(self, percept):
        # Вызывается каждый ход. Строит весь оставшийся маршрут,
        # но возвращает только следующий город.

        # 1. сохраняем матрицу, чтобы _greedy_route и _two_opt могли брать расстояния
        self.distance_matrix = percept.dist_matrix

        # 2. собираем непосещённые города
        unvisited = []
        for city in range(len(percept.cities)):
            if city not in percept.visited:
                unvisited.append(city)

        # 3. все города посещены -> едем на базу
        if len(unvisited) == 0:
            return 0

        # 4. строим маршрут: текущий город -> все непосещённые -> база
        route = self._greedy_route(percept.current_city, unvisited)

        # 5. улучшаем маршрут
        route = self._two_opt(route)

        # 6. route[0] - где мы стоим, route[1] - куда ехать сейчас
        return route[1]

    def _greedy_route(self, start, cities_to_visit):
        # Строит весь маршрут жадно: из каждого города едем в ближайший ещё не включённый.
        # Возвращает список вида [start, ..., 0], где 0 - база.
        route = [start]
        remaining = list(cities_to_visit)

        while len(remaining) > 0:
            last = route[-1]

            # ищем ближайший к последнему городу маршрута
            nearest = remaining[0]
            for city in remaining:
                if self.distance_matrix[last][city] < self.distance_matrix[last][nearest]:
                    nearest = city

            route.append(nearest)
            remaining.remove(nearest)

        route.append(0)
        return route

    def _two_opt(self, route):
        # Улучшает маршрут: переворачивает куски маршрута, если от этого он становится короче.
        # Первый город (где стоим) и последний (база) не трогаем.
        d = self.distance_matrix
        improved = True

        while improved:
            improved = False

            for i in range(1, len(route) - 2):
                for j in range(i + 1, len(route) - 1):
                    # Переворот куска route[i..j] меняет только две дороги на краях:
                    # было:  A -> B ... C -> D
                    # стало: A -> C ... B -> D
                    a = route[i - 1]
                    b = route[i]
                    c = route[j]
                    e = route[j + 1]

                    old_length = d[a][b] + d[c][e]
                    new_length = d[a][c] + d[b][e]

                    # маленький запас 1e-9 защищает от бесконечного цикла из-за погрешности float
                    if new_length < old_length - 1e-9:
                        route[i:j + 1] = route[i:j + 1][::-1]
                        improved = True

        return route
