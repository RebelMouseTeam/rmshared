from dataclasses import dataclass

from rmshared.content.taxonomy.abc import Label


@dataclass(frozen=True)
class Producer(Label):
    what: str
