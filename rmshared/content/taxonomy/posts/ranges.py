from dataclasses import dataclass


@dataclass(frozen=True)
class ModifiedBetween(Range):
    min_ts: int
    max_ts: int


@dataclass(frozen=True)
class ModifiedBefore(Range):
    ts: int


@dataclass(frozen=True)
class ModifiedAfter(Range):
    ts: int
