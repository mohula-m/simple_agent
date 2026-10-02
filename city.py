from dataclasses import dataclass


@dataclass(frozen=True)
class City:
    idx: int
    x: int
    y: int
    name: str

