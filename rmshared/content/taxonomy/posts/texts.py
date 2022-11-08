from dataclasses import dataclass

from rmshared.content.taxonomy.abc import Text


@dataclass(frozen=True)
class Titles(Text):
    pass


@dataclass(frozen=True)
class Subtitles(Text):
    pass


@dataclass(frozen=True)
class RegularTags(Text):
    pass


@dataclass(frozen=True)
class Bodies(Text):
    pass


@dataclass(frozen=True)
class CustomField(Text):
    path: str
