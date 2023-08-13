from typing import Any

from rmshared.content.taxonomy import core
from rmshared.content.taxonomy.users import fields
from rmshared.content.taxonomy.users import statuses
from rmshared.content.taxonomy.users.aspects import Aspects

Id = core.aliases.labels.SystemFieldValue[int, int](fields.Id)
Slug = core.aliases.labels.SystemFieldValue[str, str](fields.Slug)
Title = core.aliases.labels.SystemFieldValue[str, str](fields.Title)
Email = core.aliases.labels.SystemFieldValue[str, str](fields.Email)
Owner = core.aliases.labels.SystemFieldValue[int, int](fields.Owner)
Status = core.aliases.labels.SystemFieldValue[statuses.Status, str](fields.Status, Aspects().map_user_profile_status)
UserGroup = core.aliases.labels.SystemFieldValue[str, str](fields.Group)
Community = core.aliases.labels.SystemFieldValue[int, int](fields.Community)
AccessRole = core.aliases.labels.SystemFieldValue[int, int](fields.AccessRole)
CustomField = core.aliases.labels.CustomFieldValue[Any, Any](fields.CustomField)

NoEmails = core.aliases.labels.SystemFieldEmpty(fields.Email)
NoUserGroups = core.aliases.labels.SystemFieldEmpty(fields.Group)
NoCommunities = core.aliases.labels.SystemFieldEmpty(fields.Community)
NoAccessRoles = core.aliases.labels.SystemFieldEmpty(fields.AccessRole)
NoCustomField = core.aliases.labels.CustomFieldEmpty(fields.CustomField)
