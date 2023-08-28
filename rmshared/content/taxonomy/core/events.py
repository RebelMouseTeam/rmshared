from dataclasses import dataclass


@dataclass(frozen=True)
class Event:
    name: str


@dataclass(frozen=True)
class Metric:
    event: Event
    value: float
