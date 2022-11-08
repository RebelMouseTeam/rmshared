from dataclasses import dataclass

from content.taxonomy.abc import Text


@dataclass(frozen=True)
class Titles(Text):
    pass


@dataclass(frozen=True)
class Emails(Text):
    pass


@dataclass(frozen=True)
class Description(Text):
    pass


@dataclass(frozen=True)
class AboutHtml(Text):
    pass


@dataclass(frozen=True)
class CustomField(Text):
    path: str
