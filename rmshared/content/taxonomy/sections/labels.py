from typing import Any

from rmshared.content.taxonomy import core
from rmshared.content.taxonomy.sections import access
from rmshared.content.taxonomy.sections import consts
from rmshared.content.taxonomy.sections import fields
from rmshared.content.taxonomy.sections.aspects import Aspects


Id = core.aliases.labels.SystemFieldValue[int, int](fields.Id)
Path = core.aliases.labels.SystemFieldValue[str, str](fields.Path)
Slug = core.aliases.labels.SystemFieldValue[str, str](fields.Slug)
Title = core.aliases.labels.SystemFieldValue[str, str](fields.Title)
ReadOnly = core.aliases.labels.SystemFieldBadge(fields.IsReadOnly)

ParentId = core.aliases.labels.SystemFieldValue[int, int](fields.ParentId)
ParentSlug = core.aliases.labels.SystemFieldValue[str, str](fields.ParentSlug)
AncestorId = core.aliases.labels.SystemFieldValue[int, int](fields.AncestorId)
AncestorSlug = core.aliases.labels.SystemFieldValue[str, str](fields.AncestorSlug)

ReadAccess = core.aliases.labels.SystemFieldValue[access.Kind, str](fields.ReadAccess, Aspects().map_section_read_access_kind)
Visibility = core.aliases.labels.SystemFieldValue[consts.VISIBILITY.STATUS, str](fields.Visibility, Aspects().map_section_visibility_status)

OpenInNewTab = core.aliases.labels.SystemFieldBadge(fields.OpenInNewTabSetting)
AllowCommunityPosts = core.aliases.labels.SystemFieldBadge(fields.AllowCommunityPostsSetting)
HideFromEntryEditor = core.aliases.labels.SystemFieldBadge(fields.HideFromEntryEditorSetting)
LockPostsAfterPublishing = core.aliases.labels.SystemFieldBadge(fields.LockPostsAfterPublishingSetting)

ImageId = core.aliases.labels.SystemFieldValue[int, int](fields.ImageId)
NoImageId = core.aliases.labels.SystemFieldEmpty(fields.ImageId)

LinkOut = core.aliases.labels.SystemFieldValue[str, str](fields.LinkOut)
NoLinkOut = core.aliases.labels.SystemFieldEmpty(fields.LinkOut)

CustomField = core.aliases.labels.CustomFieldValue[Any, Any](fields.CustomField)
NoCustomField = core.aliases.labels.CustomFieldEmpty(fields.CustomField)
