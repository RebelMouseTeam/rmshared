from dataclasses import dataclass


@dataclass(frozen=True)
class Tag:
    slug: str


@dataclass(frozen=True)
class Section:
    id: int


@dataclass(frozen=True)
class Community:
    id: int
    slug: str
    title: str
    about_html: str
    description: str


@dataclass(frozen=True)
class Layout:
    slug: str
