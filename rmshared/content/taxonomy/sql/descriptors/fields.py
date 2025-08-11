from __future__ import annotations

from rmshared.content.taxonomy import core
from rmshared.content.taxonomy import tags
from rmshared.content.taxonomy import posts
from rmshared.content.taxonomy import sections
from rmshared.content.taxonomy import users
from rmshared.content.taxonomy import communities

from rmshared.content.taxonomy.sql.descriptors import scopes
from rmshared.content.taxonomy.sql.descriptors import options
from rmshared.content.taxonomy.sql.descriptors.beans import Descriptor


FIELDS = (
    Descriptor(
        scope=scopes.Entity(tags.guids.Tag),
        subject=core.fields.System(name='tag-slug'),
        aliases=('slug',),
        options=frozenset({options.Id(), options.SingleValue()}),
    ),
    Descriptor(
        scope=scopes.Entity(posts.guids.Post),
        subject=posts.fields.Id(),
        aliases=('id',),
        options=frozenset({options.Id(), options.SingleValue()}),
    ),
    Descriptor(
        scope=scopes.Entity(posts.guids.Post),
        subject=posts.fields.Type(),
        aliases=('type',),
        options=frozenset({options.SingleValue()}),
    ),
    Descriptor(
        scope=scopes.Entity(posts.guids.Post),
        subject=posts.fields.Status(),
        aliases=('status',),
        options=frozenset({options.SingleValue()}),
    ),
    Descriptor(
        scope=scopes.Entity(posts.guids.Post),
        subject=posts.fields.IsPrivate(),
        aliases=('is_private',),
        options=frozenset({options.Badge()}),
    ),
    Descriptor(
        scope=scopes.Entity(posts.guids.Post),
        subject=posts.fields.IsSuspicious(),
        aliases=('is_suspicious',),
        options=frozenset({options.Badge()}),
    ),
    Descriptor(
        scope=scopes.Entity(posts.guids.Post),
        subject=posts.fields.IsExcludedFromSearch(),
        aliases=('is_excluded_from_search',),
        options=frozenset({options.Badge()}),
    ),
    Descriptor(
        scope=scopes.Entity(posts.guids.Post),
        subject=posts.fields.ModifiedAt(),
        aliases=('modified_at',),
        options=frozenset({options.SingleValue()}),
    ),
    Descriptor(
        scope=scopes.Entity(posts.guids.Post),
        subject=posts.fields.ScheduledAt(),
        aliases=('scheduled_at',),
        options=frozenset({options.SingleValue(), options.Optional()}),
    ),
    Descriptor(
        scope=scopes.Entity(posts.guids.Post),
        subject=posts.fields.PublishedAt(),
        aliases=('published_at',),
        options=frozenset({options.SingleValue(), options.Optional()}),
    ),
    Descriptor(
        scope=scopes.Entity(posts.guids.Post),
        subject=posts.fields.EmbargoedUntil(),
        aliases=('embargoed_until',),
        options=frozenset({options.SingleValue(), options.Optional()}),
    ),
    Descriptor(
        scope=scopes.Entity(posts.guids.Post),
        subject=posts.fields.Title(),
        aliases=('title',),
        options=frozenset({options.SingleValue()}),
    ),
    Descriptor(
        scope=scopes.Entity(posts.guids.Post),
        subject=posts.fields.Subtitle(),
        aliases=('subtitles',),
        options=frozenset({options.MultiValue(), options.Optional()}),
    ),
    Descriptor(
        scope=scopes.Entity(posts.guids.Post),
        subject=posts.fields.Body(),
        aliases=('bodies',),
        options=frozenset({options.MultiValue(), options.Optional()}),
    ),
    Descriptor(
        scope=scopes.Entity(posts.guids.Post),
        subject=posts.fields.PrimaryTag(),
        aliases=('primary_tag',),
        options=frozenset({options.SingleValue(), options.Optional()}),
    ),
    Descriptor(
        scope=scopes.Entity(posts.guids.Post),
        subject=posts.fields.RegularTag(),
        aliases=('regular_tags',),
        options=frozenset({options.MultiValue(), options.Optional()}),
    ),
    Descriptor(
        scope=scopes.Entity(posts.guids.Post),
        subject=posts.fields.PrimarySection(),
        aliases=('primary_section',),
        options=frozenset({options.SingleValue(), options.Optional()}),
    ),
    Descriptor(
        scope=scopes.Entity(posts.guids.Post),
        subject=posts.fields.RegularSection(),
        aliases=('regular_sections',),
        options=frozenset({options.MultiValue(), options.Optional()}),
    ),
    Descriptor(
        scope=scopes.Entity(posts.guids.Post),
        subject=posts.fields.Community(),
        aliases=('community',),
        options=frozenset({options.SingleValue(), options.Optional()}),
    ),
    Descriptor(
        scope=scopes.Entity(posts.guids.Post),
        subject=posts.fields.Author(),
        aliases=('authors',),
        options=frozenset({options.MultiValue()}),
    ),
    Descriptor(
        scope=scopes.Entity(posts.guids.Post),
        subject=posts.fields.Stage(),
        aliases=('stage',),
        options=frozenset({options.SingleValue(), options.Optional(), options.Deprecated()}),
    ),
    Descriptor(
        scope=scopes.Entity(posts.guids.Post),
        subject=posts.fields.PageLayout(),
        aliases=('page_layout',),
        options=frozenset({options.SingleValue(), options.Optional()}),
    ),
    Descriptor(
        scope=scopes.Entity(posts.guids.Post),
        subject=posts.fields.EditorLayout(),
        aliases=('editor_layout',),
        options=frozenset({options.SingleValue(), options.Optional()}),
    ),
    Descriptor(
        scope=scopes.Entity(sections.guids.Section),
        subject=sections.fields.Id(),
        aliases=('id',),
        options=frozenset({options.Id(), options.SingleValue()}),
    ),
    Descriptor(
        scope=scopes.Entity(sections.guids.Section),
        subject=sections.fields.Path(),
        aliases=('path',),
        options=frozenset({options.SingleValue()}),
    ),
    Descriptor(
        scope=scopes.Entity(sections.guids.Section),
        subject=sections.fields.Slug(),
        aliases=('slug',),
        options=frozenset({options.SingleValue()}),
    ),
    Descriptor(
        scope=scopes.Entity(sections.guids.Section),
        subject=sections.fields.Title(),
        aliases=('title',),
        options=frozenset({options.SingleValue()}),
    ),
    Descriptor(
        scope=scopes.Entity(sections.guids.Section),
        subject=sections.fields.OrderId(),
        aliases=('order_id',),
        options=frozenset({options.SingleValue()}),
    ),
    Descriptor(
        scope=scopes.Entity(sections.guids.Section),
        subject=sections.fields.CreatedAt(),
        aliases=('created_at',),
        options=frozenset({options.SingleValue()}),
    ),
    Descriptor(
        scope=scopes.Entity(sections.guids.Section),
        subject=sections.fields.IsReadOnly(),
        aliases=('is_read_only',),
        options=frozenset({options.Badge()}),
    ),
    Descriptor(
        scope=scopes.Entity(sections.guids.Section),
        subject=sections.fields.ParentId(),
        aliases=('parent_id',),
        options=frozenset({options.SingleValue(), options.Optional()}),
    ),
    Descriptor(
        scope=scopes.Entity(sections.guids.Section),
        subject=sections.fields.AncestorId(),
        aliases=('ancestor_ids',),
        options=frozenset({options.MultiValue(), options.Optional()}),
    ),
    Descriptor(
        scope=scopes.Entity(sections.guids.Section),
        subject=sections.fields.Visibility(),
        aliases=('visibility',),
        options=frozenset({options.SingleValue()}),
    ),
    Descriptor(
        scope=scopes.Entity(sections.guids.Section),
        subject=sections.fields.ReadAccess(),
        aliases=('read_access.type',),
        options=frozenset({options.SingleValue()}),
    ),
    Descriptor(
        scope=scopes.Entity(sections.guids.Section),
        subject=sections.fields.OpenInNewTabSetting(),
        aliases=('settings.open_in_new_tab',),
        options=frozenset({options.Badge(), options.Optional()}),
    ),
    Descriptor(
        scope=scopes.Entity(sections.guids.Section),
        subject=sections.fields.AllowCommunityPostsSetting(),
        aliases=('settings.allow_community_posts',),
        options=frozenset({options.Badge(), options.Optional()}),
    ),
    Descriptor(
        scope=scopes.Entity(sections.guids.Section),
        subject=sections.fields.HideFromEntryEditorSetting(),
        aliases=('settings.hide_from_entry_editor',),
        options=frozenset({options.Badge(), options.Optional()}),
    ),
    Descriptor(
        scope=scopes.Entity(sections.guids.Section),
        subject=sections.fields.LockPostsAfterPublishingSetting(),
        aliases=('settings.lock_posts_after_publishing',),
        options=frozenset({options.Badge(), options.Optional()}),
    ),
    Descriptor(
        scope=scopes.Entity(sections.guids.Section),
        subject=sections.fields.ImageId(),
        aliases=('image.id',),
        options=frozenset({options.SingleValue(), options.Optional()}),
    ),
    Descriptor(
        scope=scopes.Entity(sections.guids.Section),
        subject=sections.fields.LinkOut(),
        aliases=('is_link_out',),
        options=frozenset({options.Badge(), options.Optional()}),
    ),
    Descriptor(
        scope=scopes.Entity(sections.guids.Section),
        subject=sections.fields.MetaTag(),
        aliases=('meta_tag',),
        options=frozenset({options.MultiValue(), options.Optional()}),
    ),
    Descriptor(
        scope=scopes.Entity(sections.guids.Section),
        subject=sections.fields.MetaTitle(),
        aliases=('meta_title',),
        options=frozenset({options.SingleValue(), options.Optional()}),
    ),
    Descriptor(
        scope=scopes.Entity(sections.guids.Section),
        subject=sections.fields.AboutHtml(),
        aliases=('about_html',),
        options=frozenset({options.SingleValue(), options.Optional()}),
    ),
    Descriptor(
        scope=scopes.Entity(users.guids.UserProfile),
        subject=users.fields.Id(),
        aliases=('profile.id', 'id',),
        options=frozenset({options.Id(), options.SingleValue()}),
    ),
    Descriptor(
        scope=scopes.Entity(users.guids.UserProfile),
        subject=users.fields.Email(),
        aliases=('emails', 'owner.emails',),
        options=frozenset({options.MultiValue()}),
    ),
    Descriptor(
        scope=scopes.Entity(users.guids.UserProfile),
        subject=users.fields.Slug(),
        aliases=('profile.slug', 'slug',),
        options=frozenset({options.SingleValue()}),
    ),
    Descriptor(
        scope=scopes.Entity(users.guids.UserProfile),
        subject=users.fields.Title(),
        aliases=('profile.title', 'title',),
        options=frozenset({options.SingleValue()}),
    ),
    Descriptor(
        scope=scopes.Entity(users.guids.UserProfile),
        subject=users.fields.Owner(),
        aliases=('profile.user_id', 'owner.id',),
        options=frozenset({options.SingleValue()}),
    ),
    Descriptor(
        scope=scopes.Entity(users.guids.UserProfile),
        subject=users.fields.Status(),
        aliases=('profile.status', 'status',),
        options=frozenset({options.SingleValue()}),
    ),
    Descriptor(
        scope=scopes.Entity(users.guids.UserProfile),
        subject=users.fields.CreatedAt(),
        aliases=('profile.created_at', 'created_at',),
        options=frozenset({options.SingleValue()}),
    ),
    Descriptor(
        scope=scopes.Entity(users.guids.UserProfile),
        subject=users.fields.AboutHtml(),
        aliases=('profile.about_html', 'about_html',),
        options=frozenset({options.SingleValue(), options.Optional()}),
    ),
    Descriptor(
        scope=scopes.Entity(users.guids.UserProfile),
        subject=users.fields.Description(),
        aliases=('profile.description', 'description',),
        options=frozenset({options.SingleValue(), options.Optional()}),
    ),
    Descriptor(
        scope=scopes.Entity(users.guids.UserProfile),
        subject=users.fields.Group(),
        aliases=('groups', 'owner.groups',),
        options=frozenset({options.MultiValue(), options.Optional()}),
    ),
    Descriptor(
        scope=scopes.Entity(users.guids.UserProfile),
        subject=users.fields.Community(),
        aliases=('community',),
        options=frozenset({options.MultiValue(), options.Optional()}),
    ),
    Descriptor(
        scope=scopes.Entity(users.guids.UserProfile),
        subject=users.fields.AccessRole(),
        aliases=('access_roles',),
        options=frozenset({options.MultiValue(), options.Optional()}),
    ),
    Descriptor(
        scope=scopes.Entity(users.guids.UserProfile),
        subject=users.fields.LastLoggedInAt(),
        aliases=('last_logged_in_at', 'owner.last_logged_in_at',),
        options=frozenset({options.SingleValue(), options.Optional()}),
    ),
    Descriptor(
        scope=scopes.Entity(communities.guids.Community),
        subject=core.fields.System(name='community-id'),
        aliases=('id',),
        options=frozenset({options.Id(), options.SingleValue()}),
    ),
)
