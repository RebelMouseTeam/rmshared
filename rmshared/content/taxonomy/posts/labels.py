from typing import Any

from rmshared.content.taxonomy import core

from rmshared.content.taxonomy.posts import consts
from rmshared.content.taxonomy.posts import fields
from rmshared.content.taxonomy.posts import statuses
from rmshared.content.taxonomy.posts.aspects import Aspects

Id = core.aliases.labels.SystemFieldValue[int, int](fields.Id)
Type = core.aliases.labels.SystemFieldValue[consts.POST.TYPE, str](fields.Type, Aspects().map_post_type)
Status = core.aliases.labels.SystemFieldValue[statuses.Status, str](fields.Status, Aspects().map_post_status)
Private = core.aliases.labels.SystemFieldBadge(fields.IsPrivate)
Suspicious = core.aliases.labels.SystemFieldBadge(fields.IsSuspicious)
ExcludedFromSearch = core.aliases.labels.SystemFieldBadge(fields.IsExcludedFromSearch)
PrimaryTag = core.aliases.labels.SystemFieldValue[str, str](fields.PrimaryTag)
RegularTag = core.aliases.labels.SystemFieldValue[str, str](fields.RegularTag)
PrimarySection = core.aliases.labels.SystemFieldValue[int, int](fields.PrimarySection)
RegularSection = core.aliases.labels.SystemFieldValue[int, int](fields.RegularSection)
Community = core.aliases.labels.SystemFieldValue[int, int](fields.Community)
Author = core.aliases.labels.SystemFieldValue[int, int](fields.Author)
Stage = core.aliases.labels.SystemFieldValue[int, int](fields.Stage)
SpecialPageLayout = core.aliases.labels.SystemFieldValue[str, str](fields.PageLayout)
SpecialEditorLayout = core.aliases.labels.SystemFieldValue[str, str](fields.EditorLayout)
CustomField = core.aliases.labels.CustomFieldValue[Any, Any](fields.CustomField)

NoPrimaryTags = core.aliases.labels.SystemFieldEmpty(fields.PrimaryTag)
NoRegularTags = core.aliases.labels.SystemFieldEmpty(fields.RegularTag)
NoPrimarySections = core.aliases.labels.SystemFieldEmpty(fields.PrimarySection)
NoRegularSections = core.aliases.labels.SystemFieldEmpty(fields.RegularSection)
NoCommunities = core.aliases.labels.SystemFieldEmpty(fields.Community)
NoAuthors = core.aliases.labels.SystemFieldEmpty(fields.Author)
NoStages = core.aliases.labels.SystemFieldEmpty(fields.Stage)
DefaultPageLayout = core.aliases.labels.SystemFieldEmpty(fields.PageLayout)
DefaultEditorLayout = core.aliases.labels.SystemFieldEmpty(fields.EditorLayout)
NoCustomField = core.aliases.labels.CustomFieldEmpty(fields.CustomField)
