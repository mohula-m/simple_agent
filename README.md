# Courier agent

Assignment 1 for UI. A courier starts at the base (city 0), has to deliver to every city and come back.
All cities are connected, but some roads are bad - a trip on a bad road can fail. When that happens
the courier stays where he was and the cost of the road is still added. The agent does not know which
roads are bad.

Two agents are compared:
- `BaselineAgent` - always goes to the nearest unvisited city
- `PlannerAgent` - plans the whole remaining route (greedy + 2-opt) every turn and goes to the first city of it

## Files

- `environment.py` - the world (cities, distances, bad roads), `step()` is the actuator, `get_percept()` is the sensor
- `percept.py` - what the agent can see
- `city.py` - city dataclass
- `BaselineAgent.py`, `PlannerAgent.py` - agents
- `main.py` - one run of every agent with the seed from config, draws the routes
- `experiment.py` - runs both agents on 20 seeds and prints mean / std
- `visualization.py` - drawing
- `config.json` - parameters

## Setup

Python 3.14 was used.

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Running

```
python main.py
python experiment.py
```

## Config

- `map_Size` - size of the map
- `cities` - number of cities (max 30, there are only 30 names)
- `seed` - seed for `main.py`, same seed = same map and same results
- `bad_ratio` - how many roads are bad (0.2 = 20 %)
- `fail_prob` - chance that a trip on a bad road fails
- `max_steps` - limit of steps, so one episode can't run forever
