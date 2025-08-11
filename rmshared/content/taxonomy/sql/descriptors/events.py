from __future__ import annotations

from rmshared.content.taxonomy import core
from rmshared.content.taxonomy import posts
from rmshared.content.taxonomy import sections
from rmshared.content.taxonomy import users

from rmshared.content.taxonomy.sql.descriptors import scopes
from rmshared.content.taxonomy.sql.descriptors import options
from rmshared.content.taxonomy.sql.descriptors.beans import Descriptor


EVENTS = (
    Descriptor(
        scope=scopes.Entity(posts.guids.Post),
        subject=posts.events.PageView(),
        aliases=('page_views',),
        options=frozenset({}),
    ),
    Descriptor(
        scope=scopes.Entity(posts.guids.Post),
        subject=posts.events.PageViewDuration(),
        aliases=('page_view_duration',),
        options=frozenset({options.NotSupported()}),
    ),
    Descriptor(
        scope=scopes.Entity(posts.guids.Post),
        subject=posts.events.TeaserView(),
        aliases=('teaser_views',),
        options=frozenset({options.NotSupported()}),
    ),
    Descriptor(
        scope=scopes.Entity(posts.guids.Post),
        subject=posts.events.TeaserClick(),
        aliases=('teaser_clicks',),
        options=frozenset({options.NotSupported()}),
    ),
    Descriptor(
        scope=scopes.Entity(sections.guids.Section),
        subject=core.events.Event('section-page-view'),
        aliases=('page_views',),
        options=frozenset({options.NotSupported()}),
    ),
    Descriptor(
        scope=scopes.Entity(sections.guids.Section),
        subject=core.events.Event('section-page-view-duration'),
        aliases=('page_view_duration',),
        options=frozenset({options.NotSupported()}),
    ),
    Descriptor(
        scope=scopes.Entity(users.guids.UserProfile),
        subject=core.events.Event('user-profile-page-view'),
        aliases=('page_views',),
        options=frozenset({options.NotSupported()}),
    ),
    Descriptor(
        scope=scopes.Entity(users.guids.UserProfile),
        subject=core.events.Event('user-profile-page-view-duration'),
        aliases=('page_view_duration',),
        options=frozenset({options.NotSupported()}),
    ),
)
