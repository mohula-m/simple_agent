class BaselineAgent:

    def act(self, percept):
        distance_temp = float("inf")
        current_city = percept.current_city
        if len(percept.visited) == len(percept.cities):
            return 0

        for i in range(len(percept.cities)):
            if distance_temp > percept.dist_matrix[current_city][i] and i != current_city and i not in percept.visited:
                distance_temp = percept.dist_matrix[current_city][i]
                chosen_city = i



        return chosen_city
