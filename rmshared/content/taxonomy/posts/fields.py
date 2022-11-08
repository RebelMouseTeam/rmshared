from dataclasses import dataclass

from rmshared.content.taxonomy.abc import Field


@dataclass(frozen=True)
class ModifiedAt(Field):
    pass


@dataclass(frozen=True)
class ScheduledAt(Field):
    pass


@dataclass(frozen=True)
class PublishedAt(Field):
    pass


@dataclass(frozen=True)
class LifetimePageViews(Field):  # TODO: == Metric(event='lifetime_page_views') ???
    pass


@dataclass(frozen=True)
class Metric(Field):
    event: str


@dataclass(frozen=True)
class CustomField(Field):
    path: str
