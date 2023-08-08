from pytest import fixture

from rmshared.content.taxonomy import core
from rmshared.content.taxonomy.users import labels
from rmshared.content.taxonomy.users import fields
from rmshared.content.taxonomy.users import statuses
from rmshared.content.taxonomy.users import mappers


class TestMappers:
    @fixture
    def factory(self) -> mappers.Factory:
        return mappers.Factory()

    def test_it_should_map_filters(self, factory: mappers.Factory):
        visitor = factory.make_visitor()
        assert tuple(visitor.visit_filters(self.USERS_FILTERS)) == tuple(self.CORE_FILTERS)

    USERS_FILTERS = [
        core.filters.AnyLabel[labels.Base](labels=(
            labels.Id(value=123),
            labels.Title(title='Title #1'),
            labels.Owner(user_id=234),
            labels.Status(status=statuses.Inactive(is_banned=True)),
            labels.Status(status=statuses.Inactive(is_banned=False)),
            labels.NoEmails(),
            labels.UserGroup(slug='group-1'),
            labels.NoCommunities(),
            labels.AccessRole(id=345),
            labels.NoCustomField(path='path.to.field_1'),
        )),
        core.filters.NoLabels[labels.Base](labels=(
            labels.Slug(slug='slug-1'),
            labels.Status(status=statuses.Pending()),
            labels.Status(status=statuses.Active()),
            labels.Email(email='email-1'),
            labels.NoUserGroups(),
            labels.Community(id=567),
            labels.NoAccessRoles(),
            labels.CustomField(path='path.to.field_2', value='value-1'),
        )),
        core.filters.AnyRange[core.ranges.Range[core.fields.Field]](ranges=(
            core.ranges.Between(field=fields.Title(), min_value='A', max_value='Z'),
            core.ranges.LessThan(field=fields.LastLoggedInAt(), value=600),
        )),
        core.filters.NoRanges[core.ranges.Range[core.fields.Field]](ranges=(
            core.ranges.MoreThan(field=fields.LastLoggedInAt(), value=50),
            core.ranges.Between(field=fields.CustomField(path='path.to.field.3'), min_value=0.01, max_value=0.99),
        )),
    ]
    CORE_FILTERS = [
        core.filters.AnyLabel[core.labels.Label](labels=(
            core.labels.Value(field=core.fields.System(name='user-id'), value=123),
            core.labels.Value(field=core.fields.System(name='user-profile-title'), value='Title #1'),
            core.labels.Value(field=core.fields.System(name='user-profile-owner'), value=234),
            core.labels.Value(field=core.fields.System(name='user-profile-status'), value='inactive(banned=true)'),
            core.labels.Value(field=core.fields.System(name='user-profile-status'), value='inactive(banned=false)'),
            core.labels.Empty(field=core.fields.System(name='user-email')),
            core.labels.Value(field=core.fields.System(name='user-group'), value='group-1'),
            core.labels.Empty(field=core.fields.System(name='user-community')),
            core.labels.Value(field=core.fields.System(name='user-access-role'), value=345),
            core.labels.Empty(field=core.fields.Custom(name='user-custom-field', path='path.to.field_1')),
        )),
        core.filters.NoLabels[core.labels.Label](labels=(
            core.labels.Value(field=core.fields.System(name='user-profile-slug'), value='slug-1'),
            core.labels.Value(field=core.fields.System(name='user-profile-status'), value='pending'),
            core.labels.Value(field=core.fields.System(name='user-profile-status'), value='active'),
            core.labels.Value(field=core.fields.System(name='user-email'), value='email-1'),
            core.labels.Empty(field=core.fields.System(name='user-group')),
            core.labels.Value(field=core.fields.System(name='user-community'), value=567),
            core.labels.Empty(field=core.fields.System(name='user-access-role')),
            core.labels.Value(field=core.fields.Custom(name='user-custom-field', path='path.to.field_2'), value='value-1'),
        )),
        core.filters.AnyRange[core.ranges.Range](ranges=(
            core.ranges.Between(field=core.fields.System(name='user-profile-title'), min_value='A', max_value='Z'),
            core.ranges.LessThan(field=core.fields.System(name='user-last-logged-in-at'), value=600),
        )),
        core.filters.NoRanges[core.ranges.Range](ranges=(
            core.ranges.MoreThan(field=core.fields.System(name='user-last-logged-in-at'), value=50),
            core.ranges.Between(field=core.fields.Custom(name='user-custom-field', path='path.to.field.3'), min_value=0.01, max_value=0.99),
        )),
    ]
