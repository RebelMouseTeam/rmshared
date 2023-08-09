from dataclasses import dataclass

from rmshared.content.taxonomy import core


@core.aliases.system_field('post-id')
@dataclass(frozen=True)
class Id:
    pass


@core.aliases.system_field('post-type')
@dataclass(frozen=True)
class Type:
    pass


@core.aliases.system_field('post-status')
@dataclass(frozen=True)
class Status:
    pass


@core.aliases.system_field('post-is-private')
@dataclass(frozen=True)
class IsPrivate:
    pass


@core.aliases.system_field('post-is-suspicious')
@dataclass(frozen=True)
class IsSuspicious:
    pass


@core.aliases.system_field('post-is-excluded-from-search')
@dataclass(frozen=True)
class IsExcludedFromSearch:
    pass


@core.aliases.system_field('post-modified-at')
@dataclass(frozen=True)
class ModifiedAt:
    pass


@core.aliases.system_field('post-scheduled-at')
@dataclass(frozen=True)
class ScheduledAt:
    pass


@core.aliases.system_field('post-published-at')
@dataclass(frozen=True)
class PublishedAt:
    pass


@core.aliases.system_field('post-title')
@dataclass(frozen=True)
class Title:
    pass


@core.aliases.system_field('post-subtitle')
@dataclass(frozen=True)
class Subtitle:
    pass


@core.aliases.system_field('post-body')
@dataclass(frozen=True)
class Body:
    pass


@core.aliases.system_field('post-primary-tag')
@dataclass(frozen=True)
class PrimaryTag:
    pass


@core.aliases.system_field('post-regular-tag')
@dataclass(frozen=True)
class RegularTag:
    pass


@core.aliases.system_field('post-primary-section')
@dataclass(frozen=True)
class PrimarySection:
    pass


@core.aliases.system_field('post-regular-section')
@dataclass(frozen=True)
class RegularSection:
    pass


@core.aliases.system_field('post-community')
@dataclass(frozen=True)
class Community:
    pass


@core.aliases.system_field('post-author')
@dataclass(frozen=True)
class Author:
    pass


@core.aliases.system_field('post-stage')
@dataclass(frozen=True)
class Stage:
    pass


@core.aliases.system_field('post-page-layout')
@dataclass(frozen=True)
class PageLayout:
    pass


@core.aliases.system_field('post-editor-layout')
@dataclass(frozen=True)
class EditorLayout:
    pass


@core.aliases.custom_field('post-custom-field')
@dataclass(frozen=True)
class CustomField:
    path: str
