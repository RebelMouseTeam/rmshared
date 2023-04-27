from rmshared.tools import ensure_map_is_complete

from rmshared.content.taxonomy import core as taxonomy_core
from rmshared.content.taxonomy import visitors as taxonomy_visitors

from rmshared.content.taxonomy.users import labels
from rmshared.content.taxonomy.users import fields
from rmshared.content.taxonomy.users import consts
from rmshared.content.taxonomy.users import statuses


class Factory:
    def __init__(self):
        self.delegate = taxonomy_core.mapper.Factory()
        self.aspects = self.Aspects()

    def make_visitor(self) -> taxonomy_visitors.IVisitor:
        builder = taxonomy_visitors.Builder()
        builder.customize_labels(self._make_labels, dependencies=())
        builder.customize_fields(self._make_fields, dependencies=())
        builder.customize_filters(self.delegate.make_filters, dependencies=(taxonomy_visitors.ILabels, taxonomy_visitors.IRanges))
        builder.customize_orders(self.delegate.make_orders, dependencies=())
        builder.customize_ranges(self.delegate.make_ranges, dependencies=(taxonomy_visitors.IFields, taxonomy_visitors.IValues))
        builder.customize_values(self.delegate.make_values, dependencies=())
        return builder.make_visitor()

    def _make_labels(self) -> taxonomy_visitors.ILabels:
        return self.Labels(self.aspects)

    def _make_fields(self) -> taxonomy_visitors.IFields:
        return self.Fields()

    class Labels(taxonomy_visitors.ILabels[labels.Base, taxonomy_core.labels.Label]):
        def __init__(self, aspects: 'Factory.Aspects'):
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
                labels.NoEmails: lambda _: taxonomy_core.labels.Empty(field=taxonomy_core.fields.System('user-email')),
                labels.NoUserGroups: lambda _: taxonomy_core.labels.Empty(field=taxonomy_core.fields.System('user-group')),
                labels.NoCommunities: lambda _: taxonomy_core.labels.Empty(field=taxonomy_core.fields.System('user-community')),
                labels.NoAccessRoles: lambda _: taxonomy_core.labels.Empty(field=taxonomy_core.fields.System('user-access-role')),
                labels.CustomField: self._map_custom_user_profile_field,
                labels.NoCustomField: self._map_no_custom_user_profile_field,
            })

        def visit_label(self, label):
            return self.label_to_factory_func_map[type(label)](label)

        @staticmethod
        def _map_user_profile_id(label: labels.Id) -> taxonomy_core.labels.Value:
            return taxonomy_core.labels.Value(field=taxonomy_core.fields.System('user-id'), value=label.value)

        @staticmethod
        def _map_user_profile_slug(label: labels.Slug) -> taxonomy_core.labels.Value:
            return taxonomy_core.labels.Value(field=taxonomy_core.fields.System('user-profile-slug'), value=label.slug)

        @staticmethod
        def _map_user_profile_title(label: labels.Title) -> taxonomy_core.labels.Value:
            return taxonomy_core.labels.Value(field=taxonomy_core.fields.System('user-profile-title'), value=label.title)

        @staticmethod
        def _map_user_email(label: labels.Email) -> taxonomy_core.labels.Value:
            return taxonomy_core.labels.Value(field=taxonomy_core.fields.System('user-email'), value=label.email)

        @staticmethod
        def _map_user_profile_owner(label: labels.Owner) -> taxonomy_core.labels.Value:
            return taxonomy_core.labels.Value(field=taxonomy_core.fields.System('user-owner'), value=label.user_id)

        def _map_user_profile_status(self, label: labels.Status) -> taxonomy_core.labels.Value:
            return taxonomy_core.labels.Value(field=taxonomy_core.fields.System('user-status'), value=self.aspects.map_user_profile_status(label.status))

        @staticmethod
        def _map_user_group(label: labels.UserGroup) -> taxonomy_core.labels.Value:
            return taxonomy_core.labels.Value(field=taxonomy_core.fields.System('user-group'), value=label.slug)

        @staticmethod
        def _map_user_community(label: labels.Community) -> taxonomy_core.labels.Value:
            return taxonomy_core.labels.Value(field=taxonomy_core.fields.System('user-community'), value=label.id)

        @staticmethod
        def _map_user_access_role(label: labels.AccessRole) -> taxonomy_core.labels.Value:
            return taxonomy_core.labels.Value(field=taxonomy_core.fields.System('user-access-role'), value=label.id)

        @staticmethod
        def _map_custom_user_profile_field(label: labels.CustomField) -> taxonomy_core.labels.Value:
            return taxonomy_core.labels.Value(field=taxonomy_core.fields.Custom('user-custom-field', path=label.path), value=label.value)

        @staticmethod
        def _map_no_custom_user_profile_field(label: labels.NoCustomField) -> taxonomy_core.labels.Empty:
            return taxonomy_core.labels.Empty(field=taxonomy_core.fields.Custom('user-custom-field', path=label.path))

    class Fields(taxonomy_visitors.IFields[fields.Base, taxonomy_core.fields.Field]):
        def __init__(self):
            self.field_to_factory_func_map = ensure_map_is_complete(fields.Base, {
                fields.Title: lambda _: taxonomy_core.fields.System('user-profile-title'),
                fields.LastLoggedInAt: lambda _: taxonomy_core.fields.System('user-last-logged-in-at'),
                fields.CustomField: self._map_custom_user_field,
            })

        def visit_field(self, field):
            return self.field_to_factory_func_map[type(field)](field)

        @staticmethod
        def _map_custom_user_field(field: fields.CustomField) -> taxonomy_core.fields.Field:
            return taxonomy_core.fields.Custom('user-custom-field', path=field.path)

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
