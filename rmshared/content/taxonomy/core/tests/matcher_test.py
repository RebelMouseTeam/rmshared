from pytest import fixture

from rmshared.units import Hours
from rmshared.units import Days

from rmshared.content.taxonomy.core import fields
from rmshared.content.taxonomy.core import labels
from rmshared.content.taxonomy.core import ranges
from rmshared.content.taxonomy.core import filters
from rmshared.content.taxonomy.core.abc import IEntity
from rmshared.content.taxonomy.core.matcher import Matcher


class TestMatcher:
    NOW = 1440000000

    @fixture
    def matcher(self) -> Matcher:
        return Matcher()

    def test_it_should_check_if_entity_matches_filters(self, matcher: Matcher):
        entity = self.Entity()
        week_ago: int = self.NOW - Days(7)

        assert matcher.does_entity_match_filters(entity, filters_=frozenset({
            filters.AnyLabel(labels=(labels.Value(field=self.FIELDS.POST_ID, value=123456), labels.Value(field=self.FIELDS.USER_ID, value=654321))),
        }))
        assert matcher.does_entity_match_filters(entity, filters_=frozenset({
            filters.NoLabels(labels=(labels.Value(field=self.FIELDS.USER_ID, value=123456),)),
        }))
        assert matcher.does_entity_match_filters(entity, filters_=frozenset({
            filters.NoLabels(labels=(labels.Value(field=self.FIELDS.POST_ID, value=654321),)),
        }))
        assert not matcher.does_entity_match_filters(entity, filters_=frozenset({
            filters.AnyLabel(labels=(labels.Value(field=self.FIELDS.USER_ID, value=123456),)),
        }))
        assert not matcher.does_entity_match_filters(entity, filters_=frozenset({
            filters.AnyLabel(labels=(labels.Value(field=self.FIELDS.POST_ID, value=654321),)),
        }))

        assert matcher.does_entity_match_filters(entity, filters_=frozenset({
            filters.AnyLabel(labels=(labels.Value(field=self.FIELDS.POST_ID, value=123456),)),
            filters.AnyLabel(labels=(labels.Badge(field=self.FIELDS.POST_PRIVATE),)),
        }))
        assert not matcher.does_entity_match_filters(entity, filters_=frozenset({
            filters.AnyLabel(labels=(labels.Value(field=self.FIELDS.POST_ID, value=123456),)),
            filters.NoLabels(labels=(labels.Badge(field=self.FIELDS.POST_PRIVATE),)),
        }))

        assert matcher.does_entity_match_filters(entity, filters_=frozenset({
            filters.AnyLabel(labels=(labels.Value(field=self.FIELDS.POST_ID, value=123456),)),
            filters.AnyLabel(labels=(labels.Empty(field=self.FIELDS.POST_STAGE),)),
        }))
        assert not matcher.does_entity_match_filters(entity, filters_=frozenset({
            filters.AnyLabel(labels=(labels.Value(field=self.FIELDS.POST_ID, value=123456),)),
            filters.NoLabels(labels=(labels.Empty(field=self.FIELDS.POST_STAGE),)),
        }))

        assert matcher.does_entity_match_filters(entity, filters_=frozenset({
            filters.AnyLabel(labels=(labels.Value(field=self.FIELDS.POST_ID, value=123456),)),
            filters.AnyRange(ranges=(ranges.MoreThan(field=self.FIELDS.POST_MODIFIED_AT, value=0),)),
            filters.AnyRange(ranges=(ranges.MoreThan(field=self.FIELDS.POST_PUBLISHED_AT, value=0),)),
        }))
        assert not matcher.does_entity_match_filters(entity, filters_=frozenset({
            filters.AnyLabel(labels=(labels.Value(field=self.FIELDS.POST_ID, value=123456),)),
            filters.AnyRange(ranges=(ranges.MoreThan(field=self.FIELDS.POST_MODIFIED_AT, value=0),)),
            filters.NoRanges(ranges=(ranges.MoreThan(field=self.FIELDS.POST_PUBLISHED_AT, value=0),)),
        }))

        assert matcher.does_entity_match_filters(entity, filters_=frozenset({
            filters.AnyLabel(labels=(labels.Value(field=self.FIELDS.POST_ID, value=123456),)),
            filters.AnyRange(ranges=(ranges.MoreThan(field=self.FIELDS.POST_MODIFIED_AT, value=0),)),
            filters.AnyRange(ranges=(ranges.LessThan(field=self.FIELDS.POST_PUBLISHED_AT, value=week_ago),)),
        }))
        assert not matcher.does_entity_match_filters(entity, filters_=frozenset({
            filters.AnyLabel(labels=(labels.Value(field=self.FIELDS.POST_ID, value=123456),)),
            filters.AnyRange(ranges=(ranges.MoreThan(field=self.FIELDS.POST_MODIFIED_AT, value=0),)),
            filters.AnyRange(ranges=(ranges.LessThan(field=self.FIELDS.POST_PUBLISHED_AT, value=week_ago - Hours(1)),)),
        }))
        assert matcher.does_entity_match_filters(entity, filters_=frozenset({
            filters.AnyLabel(labels=(labels.Value(field=self.FIELDS.POST_ID, value=123456),)),
            filters.AnyRange(ranges=(ranges.MoreThan(field=self.FIELDS.POST_MODIFIED_AT, value=0),)),
            filters.AnyRange(ranges=(ranges.Between(field=self.FIELDS.POST_PUBLISHED_AT, min_value=week_ago - Hours(1), max_value=week_ago + Hours(2)),)),
        }))
        assert not matcher.does_entity_match_filters(entity, filters_=frozenset({
            filters.AnyLabel(labels=(labels.Value(field=self.FIELDS.POST_ID, value=123456),)),
            filters.AnyRange(ranges=(ranges.MoreThan(field=self.FIELDS.POST_MODIFIED_AT, value=0),)),
            filters.AnyRange(ranges=(ranges.Between(field=self.FIELDS.POST_PUBLISHED_AT, min_value=week_ago + Hours(1), max_value=week_ago + Hours(2)),)),
        }))
        assert matcher.does_entity_match_filters(entity, filters_=frozenset({
            filters.AnyLabel(labels=(labels.Value(field=self.FIELDS.POST_ID, value=123456),)),
            filters.AnyRange(ranges=(ranges.MoreThan(field=self.FIELDS.POST_MODIFIED_AT, value=week_ago - Hours(1)),)),
            filters.AnyRange(ranges=(ranges.Between(field=self.FIELDS.POST_PUBLISHED_AT, min_value=week_ago - Hours(1), max_value=week_ago + Hours(2)),)),
        }))

    class Entity(IEntity[str | int | float | bool]):
        def __init__(self):
            self.field_to_values_map = {
                TestMatcher.FIELDS.POST_ID: frozenset({123456}),
                TestMatcher.FIELDS.POST_TYPE: frozenset({'page'}),
                TestMatcher.FIELDS.POST_STATUS: frozenset({'published-to-site(promoted=false)'}),
                TestMatcher.FIELDS.POST_PRIVATE: frozenset({True}),
                TestMatcher.FIELDS.POST_PRIMARY_TAG: frozenset({'tag-1'}),
                TestMatcher.FIELDS.POST_REGULAR_TAG: frozenset({'tag-1', 'tag-2'}),
                TestMatcher.FIELDS.POST_PRIMARY_SECTION: frozenset({123}),
                TestMatcher.FIELDS.POST_REGULAR_SECTION: frozenset({123}),
                TestMatcher.FIELDS.POST_STAGE: frozenset({}),
                TestMatcher.FIELDS.POST_MODIFIED_AT: frozenset({TestMatcher.NOW - Days(3)}),
                TestMatcher.FIELDS.POST_PUBLISHED_AT: frozenset({TestMatcher.NOW - Days(7)}),
            }

        def get_values(self, field):
            return frozenset(self.field_to_values_map.get(field, frozenset()))

    class FIELDS:
        USER_ID = fields.System(name='user-id')
        POST_ID = fields.System(name='post-id')
        POST_TYPE = fields.System(name='post-type')
        POST_STATUS = fields.System(name='post-status')
        POST_PRIVATE = fields.System(name='post-private')
        POST_PRIMARY_TAG = fields.System(name='post-primary-tag')
        POST_REGULAR_TAG = fields.System(name='post-regular-tag')
        POST_PRIMARY_SECTION = fields.System(name='post-primary-section')
        POST_REGULAR_SECTION = fields.System(name='post-regular-section')
        POST_COMMUNITY = fields.System(name='post-community')
        POST_AUTHOR = fields.System(name='post-author')
        POST_STAGE = fields.System(name='post-stage')
        POST_MODIFIED_AT = fields.System(name='post-modified-at')
        POST_PUBLISHED_AT = fields.System(name='post-published-at')
