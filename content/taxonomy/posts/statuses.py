from abc import ABCMeta
from dataclasses import dataclass

from content.taxonomy.posts import drafts
from content.taxonomy.posts import published


class Status(metaclass=ABCMeta):
    pass


@dataclass(frozen=True)
class Draft(Status):
    stage: drafts.stages.Stage


@dataclass(frozen=True)
class Published(Status):
    scope: published.scopes.Scope


@dataclass(frozen=True)
class Removed(Status):
    pass
