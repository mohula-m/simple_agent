import json
import statistics
import time

from environment import Environment
from BaselineAgent import BaselineAgent
from MemoryAgent import MemoryAgent

def run_episode(env, agent, max_steps):
    # time is measured only for the agent's decisions, not for the environment
    decision_time = 0.0

    while not env.is_done() and env.steps < max_steps:
        percept = env.get_percept()

        start = time.perf_counter()
        target = agent.act(percept)
        decision_time += time.perf_counter() - start

        env.step(target)

    return {
        "total_cost": env.total_cost,
        "steps": env.steps,
        "failures": env.failures,
        "completed": env.is_done(),
        "time_ms": decision_time * 1000,
    }

with open("config.json", "r") as config_file:
    config_data = json.load(config_file)

settings = config_data["environmentSettings"]
MAX_STEPS = config_data["experimentSettings"]["max_steps"]
SEEDS = range(1, 21)

baseline_results = []
memory_results = []

for seed in SEEDS:
    env = Environment(settings["map_Size"], settings["cities"], seed,
                      settings["bad_ratio"], settings["fail_prob"])
    baseline_result = run_episode(env, BaselineAgent(), MAX_STEPS)

    env = Environment(settings["map_Size"], settings["cities"], seed,
                      settings["bad_ratio"], settings["fail_prob"])
    memory_result = run_episode(env, MemoryAgent(), MAX_STEPS)

    baseline_results.append(baseline_result)
    memory_results.append(memory_result)
    print(f"seed {seed:2}: baseline {baseline_result['total_cost']:8.1f} ({baseline_result['time_ms']:6.2f} ms)"
          f" | memory {memory_result['total_cost']:8.1f} ({memory_result['time_ms']:6.2f} ms)")



def print_summary(name, results):
    costs = []
    steps = []
    failures = []
    times = []
    for result in results:
        costs.append(result["total_cost"])
        steps.append(result["steps"])
        failures.append(result["failures"])
        times.append(result["time_ms"])

    print(f"{name}: cost {statistics.mean(costs):.1f} +- {statistics.stdev(costs):.1f}"
          f" | steps {statistics.mean(steps):.1f} +- {statistics.stdev(steps):.1f}"
          f" | failures {statistics.mean(failures):.1f}"
          f" | time {statistics.mean(times):.2f} ms")


print()
print_summary("Baseline", baseline_results)
print_summary("Memory  ", memory_results)
