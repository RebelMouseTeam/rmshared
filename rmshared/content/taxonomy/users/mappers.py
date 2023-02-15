from typing import Any
from typing import Mapping

from rmshared.tools import ensure_map_is_complete
from rmshared.tools import invert_dict
from rmshared.tools import parse_name_and_info

from rmshared.content.taxonomy import core
from rmshared.content.taxonomy import mappers
from rmshared.content.taxonomy.abc import Text

from rmshared.content.taxonomy.users import labels
from rmshared.content.taxonomy.users import fields
from rmshared.content.taxonomy.users import consts
from rmshared.content.taxonomy.users import statuses
from rmshared.content.taxonomy.users import texts


class Labels(mappers.ILabels[labels.Base]):
    def __init__(self, aspects: 'Aspects'):
        self.aspects = aspects
        self.label_to_factory_func_map = ensure_map_is_complete(labels.Base, {
            labels.Id: self._map_user_profile_id,
            labels.Slug: self._map_user_profile_slug,
            labels.Title: self._map_user_profile_title,
            labels.Email: self._map_user_email,
            labels.Owner: self._map_user_profile_owner,
            labels.Status: self._map_user_profile_status,
            labels.UserGroup: self._map_user_group,
            labels.Community: self._map_user_community,
            labels.AccessRole: self._map_user_access_role,
            labels.NoEmails: lambda _: core.labels.Empty(field=core.fields.System('user-email')),
            labels.NoUserGroups: lambda _: core.labels.Empty(field=core.fields.System('user-group')),
            labels.NoCommunities: lambda _: core.labels.Empty(field=core.fields.System('user-community')),
            labels.NoAccessRoles: lambda _: core.labels.Empty(field=core.fields.System('user-access-role')),
            labels.CustomField: self._map_custom_user_profile_field,
            labels.NoCustomField: self._map_no_custom_user_profile_field,
        })

    def map_label(self, label):
        return self.label_to_factory_func_map[type(label)](label)

    @staticmethod
    def _map_user_profile_id(label: labels.Id) -> core.labels.Value:
        return core.labels.Value(field=core.fields.System('user-id'), value=label.value)

    @staticmethod
    def _map_user_profile_slug(label: labels.Slug) -> core.labels.Value:
        return core.labels.Value(field=core.fields.System('user-profile-slug'), value=label.slug)

    @staticmethod
    def _map_user_profile_title(label: labels.Title) -> core.labels.Value:
        return core.labels.Value(field=core.fields.System('user-profile-title'), value=label.title)

    @staticmethod
    def _map_user_email(label: labels.Email) -> core.labels.Value:
        return core.labels.Value(field=core.fields.System('user-email'), value=label.email)

    @staticmethod
    def _map_user_profile_owner(label: labels.Owner) -> core.labels.Value:
        return core.labels.Value(field=core.fields.System('user-owner'), value=label.user_id)

    def _map_user_profile_status(self, label: labels.Status) -> core.labels.Value:
        return core.labels.Value(field=core.fields.System('user-status'), value=self.aspects.map_user_profile_status(label.status))

    @staticmethod
    def _map_user_group(label: labels.UserGroup) -> core.labels.Value:
        return core.labels.Value(field=core.fields.System('user-group'), value=label.slug)

    @staticmethod
    def _map_user_community(label: labels.Community) -> core.labels.Value:
        return core.labels.Value(field=core.fields.System('user-community'), value=label.id)

    @staticmethod
    def _map_user_access_role(label: labels.AccessRole) -> core.labels.Value:
        return core.labels.Value(field=core.fields.System('user-access-role'), value=label.id)

    @staticmethod
    def _map_custom_user_profile_field(label: labels.CustomField) -> core.labels.Value:
        return core.labels.Value(field=core.fields.Custom('custom-user-field', path=label.path), value=label.value)

    @staticmethod
    def _map_no_custom_user_profile_field(label: labels.NoCustomField) -> core.labels.Empty:
        return core.labels.Empty(field=core.fields.Custom('custom-user-field', path=label.path))


class Fields(mappers.IFields[fields.Base]):
    def __init__(self):
        self.field_to_factory_func_map = ensure_map_is_complete(fields.Base, {
            fields.Title: lambda _: core.fields.System('user-profile-title'),
            fields.LastLoggedInAt: lambda _: core.fields.System('user-last-logged-in-at'),
            fields.LifetimePosts: lambda _: core.fields.System('lifetime-user-posts'),
            fields.CustomField: self._map_custom_user_field,
        })

    def map_field(self, field):
        return self.field_to_factory_func_map[type(field)](field)

    @staticmethod
    def _map_custom_user_field(field: fields.CustomField) -> core.Field:
        return core.fields.Custom('custom-user-field', path=field.path)


class Aspects:
    def __init__(self):
        self.user_status_to_factory_func_map = ensure_map_is_complete(statuses.Status, {
            statuses.Active: lambda _: 'active',
            statuses.Pending: lambda _: 'pending',
            statuses.Inactive: self._map_inactive_user_profile_status,
        })

    def map_user_profile_status(self, status: statuses.Status) -> str:
        return self.user_status_to_factory_func_map[type(status)](status)

    @staticmethod
    def _map_inactive_user_profile_status(status: statuses.Inactive) -> str:
        return f'inactive(banned={str(status.is_banned).lower()})'

    def map_user_status(self, status: consts.USER.STATUS) -> str:
        return self.USER_STATUS_TO_ID_MAP[status]

    USER_STATUS_TO_ID_MAP = {
        consts.USER.STATUS.ACTIVE: 'active',
        consts.USER.STATUS.INACTIVE: 'inactive',
    }
    assert set(USER_STATUS_TO_ID_MAP.keys()) == consts.USER.STATUS.ALL


class Texts:
    def __init__(self):
        self.text_to_name_map = ensure_map_is_complete(Text, {
            texts.Titles: 'user-titles',
            texts.Emails: 'user-emails',
            texts.AboutHtml: 'user-about-html',
            texts.Description: 'user-description',
            texts.CustomField: 'custom-user-field',
        })
        self.text_from_name_map = invert_dict(self.text_to_name_map)
        self.text_to_info_func_map = ensure_map_is_complete(Text, {
            texts.Titles: lambda _: dict(),
            texts.Emails: lambda _: dict(),
            texts.AboutHtml: lambda _: dict(),
            texts.Description: lambda _: dict(),
            texts.CustomField: self._jsonify_custom_user_field,
        })
        self.text_to_factory_func_map = ensure_map_is_complete(Text, {
            texts.Titles: lambda _: texts.Titles(),
            texts.Emails: lambda _: texts.Emails(),
            texts.AboutHtml: lambda _: texts.AboutHtml(),
            texts.Description: lambda _: texts.Description(),
            texts.CustomField: self._map_custom_user_field,
        })

    def jsonify_text(self, text: Text) -> Mapping[str, Any]:
        name = self.text_to_name_map[type(text)]
        info = self.text_to_info_func_map[type(text)](text)
        return {name: info}

    def map_text(self, data: Mapping[str, Any]) -> Text:
        name, info = parse_name_and_info(data)
        text_type = self.text_from_name_map[name]
        return self.text_to_factory_func_map[text_type](info)

    @staticmethod
    def _jsonify_custom_user_field(text: texts.CustomField):
        return {'path': text.path}

    @staticmethod
    def _map_custom_user_field(data: Mapping[str, Any]) -> texts.CustomField:
        return texts.CustomField(path=str(data['path']))
