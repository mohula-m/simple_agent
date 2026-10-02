import json
from environment import Environment
from visualization import draw_map


with open("config.json", "r") as config_file:
    config_data = json.load(config_file)

MAP_SIZE = config_data["environmentSettings"]["map_Size"]
CITIES_COUNT = config_data["environmentSettings"]["cities"]
SEED = config_data["environmentSettings"]["seed"]
BAD_RATIO = config_data["environmentSettings"]["bad_ratio"]
FAIL_PROBABILITY = config_data["environmentSettings"]["fail_prob"]
MAX_STEPS = config_data["experimentSettings"]["max_steps"]



env = Environment(MAP_SIZE, CITIES_COUNT, SEED, BAD_RATIO, FAIL_PROBABILITY)

print(env.cities)
print(env.bad_routes)

for i in range(env.cities_count):
    for j in range(env.cities_count):
        print(env.dist_matrix[i][j], " ", end='')
    print()

draw_map(env.cities, env.map_size)
