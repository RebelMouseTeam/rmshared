from abc import ABCMeta
from dataclasses import dataclass

from rmshared.content.taxonomy.posts import drafts
from rmshared.content.taxonomy.posts import published


@dataclass(frozen=True)
class Status(metaclass=ABCMeta):
    ...


@dataclass(frozen=True)
class Draft(Status):
    stage: drafts.stages.Stage


@dataclass(frozen=True)
class Published(Status):
    scope: published.scopes.Scope


@dataclass(frozen=True)
class Removed(Status):
    pass
