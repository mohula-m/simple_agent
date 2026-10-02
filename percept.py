from dataclasses import dataclass

from city import City


@dataclass(frozen=True)
class Percept:
    current_city: int
    cities: tuple[City, ...]
    visited: frozenset[int]
    last_success: bool
    dist_matrix: list[list[float]]