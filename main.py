import json

from BaselineAgent import BaselineAgent
from PlannerAgent import PlannerAgent
from environment import Environment
from visualization import draw_map, draw_route
import matplotlib.pyplot as plt


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
print("--------------------------------------GOING AROUNG ---------------------------------------------------------")

print("Bad roads:", sorted(env.bad_routes))
print("Start:", env.get_percept().current_city, env.get_percept().visited, "done =", env.is_done())

# visit all cities in index order and return to the base
order_route = [env.base]  # cities in the order they were actually reached
for target in list(range(1, env.cities_count)) + [env.base]:
    while True:
        success = env.step(target)
        print(f"step {env.steps}: -> {target}  {'OK' if success else 'FAIL'}  cost={env.total_cost:.1f}")
        if success:
            order_route.append(target)
            break

print("End: done =", env.is_done(), "| steps:", env.steps, "| failures:", env.failures,
      "| cost:", round(env.total_cost, 2))
order_title = f"In order: cost {env.total_cost:.1f}, failures {env.failures}"

env = Environment(MAP_SIZE, CITIES_COUNT, SEED, BAD_RATIO, FAIL_PROBABILITY)

print("--------------------------------------BASELINE AGENT ---------------------------------------------------------")
print("Bad roads:", sorted(env.bad_routes))
print("Start:", env.get_percept().current_city, env.get_percept().visited, "done =", env.is_done())

agent = BaselineAgent()
baseline_route = [env.base]
while not env.is_done() and env.steps < MAX_STEPS:
    target = agent.act(env.get_percept())
    success = env.step(target)
    print(f"step {env.steps}: -> {target}  {'OK' if success else 'FAIL'}  cost={env.total_cost:.1f}")
    if success:
        baseline_route.append(target)
print("done =", env.is_done(), "| steps:", env.steps, "| failures:", env.failures, "total_cost=", round(env.total_cost, 2), "|")
baseline_title = f"Baseline (greedy): cost {env.total_cost:.1f}, failures {env.failures}"

print("--------------------------------------BASELINE AGENT ---------------------------------------------------------")

env = Environment(MAP_SIZE, CITIES_COUNT, SEED, BAD_RATIO, FAIL_PROBABILITY)

print("--------------------------------------PLANNER AGENT ----------------------------------------------------------")
print("Bad roads:", sorted(env.bad_routes))
print("Start:", env.get_percept().current_city, env.get_percept().visited, "done =", env.is_done())

agent = PlannerAgent()
planner_route = [env.base]
while not env.is_done() and env.steps < MAX_STEPS:
    target = agent.act(env.get_percept())
    success = env.step(target)
    print(f"step {env.steps}: -> {target}  {'OK' if success else 'FAIL'}  cost={env.total_cost:.1f}")
    if success:
        planner_route.append(target)
print("done =", env.is_done(), "| steps:", env.steps, "| failures:", env.failures, "total_cost=", round(env.total_cost, 2), "|")
planner_title = f"Planner (greedy + 2-opt): cost {env.total_cost:.1f}, failures {env.failures}"

# Draw routes: three separate windows, all opened at the same time
draw_route(env.cities, order_route, env.bad_routes, env.map_size, order_title)
draw_route(env.cities, baseline_route, env.bad_routes, env.map_size, baseline_title)
draw_route(env.cities, planner_route, env.bad_routes, env.map_size, planner_title)
plt.show()
