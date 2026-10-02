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

print("Плохие дороги:", sorted(env.bad_routes))
print("Начало:", env.get_percept().current_city, env.get_percept().visited, "done =", env.is_done())

# объехать все города по порядку номеров и вернуться на базу
for target in list(range(1, env.cities_count)) + [env.base]:
    while True:
        success = env.step(target)
        print(f"шаг {env.steps}: -> {target}  {'OK' if success else 'ПРОВАЛ'}  cost={env.total_cost:.1f}")
        if success:
            break

print("Конец: done =", env.is_done(), "| шагов:", env.steps, "| провалов:", env.failures,
      "| стоимость:", round(env.total_cost, 2))
