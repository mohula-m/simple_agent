import json
import statistics

from environment import Environment
from BaselineAgent import BaselineAgent
from PlannerAgent import PlannerAgent

def run_episode(env, agent, max_steps):
    while not env.is_done() and env.steps < max_steps:
        target = agent.act(env.get_percept())
        env.step(target)

    return {
        "total_cost": env.total_cost,
        "steps": env.steps,
        "failures": env.failures,
        "completed": env.is_done(),
    }

with open("config.json", "r") as config_file:
    config_data = json.load(config_file)

settings = config_data["environmentSettings"]
MAX_STEPS = config_data["experimentSettings"]["max_steps"]
SEEDS = range(1, 21)

baseline_costs = []
planner_costs = []

for seed in SEEDS:
    env = Environment(settings["map_Size"], settings["cities"], seed,
                      settings["bad_ratio"], settings["fail_prob"])
    baseline_result = run_episode(env, BaselineAgent(), MAX_STEPS)

    env = Environment(settings["map_Size"], settings["cities"], seed,
                      settings["bad_ratio"], settings["fail_prob"])
    planner_result = run_episode(env, PlannerAgent(), MAX_STEPS)

    baseline_costs.append(baseline_result["total_cost"])
    planner_costs.append(planner_result["total_cost"])
    print(f"seed {seed:2}: baseline {baseline_result['total_cost']:8.1f} | planner {planner_result['total_cost']:8.1f}")

print()
print(f"Baseline: среднее {statistics.mean(baseline_costs):.1f}, std {statistics.stdev(baseline_costs):.1f}")
print(f"Planner:  среднее {statistics.mean(planner_costs):.1f}, std {statistics.stdev(planner_costs):.1f}")