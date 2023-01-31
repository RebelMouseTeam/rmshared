from pytest import fixture

from rmshared.units import Hours
from rmshared.units import Days

from rmshared.content.taxonomy.core import ranges
from rmshared.content.taxonomy.core import labels
from rmshared.content.taxonomy.core import filters
from rmshared.content.taxonomy.core.abc import Value
from rmshared.content.taxonomy.core.matcher import Matcher


class TestMarcher:
    NOW = 1440000000

    @fixture
    def matcher(self) -> Matcher:
        return Matcher()

    def test_it_should_check_id_post_aspects_match_filters(self, matcher: Matcher):
        aspects = self.Aspects()
        week_ago: int = TestMarcher.NOW - Days(7)

        assert matcher.do_aspects_match_filters(aspects, filters_=frozenset({
            filters.AnyLabel(labels=(labels.Value(field='post-id', value=123456), labels.Value(field='user-id', value=654321))),
        }))
        assert matcher.do_aspects_match_filters(aspects, filters_=frozenset({
            filters.NoLabels(labels=(labels.Value(field='user-id', value=123456),)),
        }))
        assert matcher.do_aspects_match_filters(aspects, filters_=frozenset({
            filters.NoLabels(labels=(labels.Value(field='post-id', value=654321),)),
        }))
        assert not matcher.do_aspects_match_filters(aspects, filters_=frozenset({
            filters.AnyLabel(labels=(labels.Value(field='user-id', value=123456), )),
        }))
        assert not matcher.do_aspects_match_filters(aspects, filters_=frozenset({
            filters.AnyLabel(labels=(labels.Value(field='post-id', value=654321), )),
        }))

        assert matcher.do_aspects_match_filters(aspects, filters_=frozenset({
            filters.AnyLabel(labels=(labels.Value(field='post-id', value=123456), )),
            filters.AnyLabel(labels=(labels.Badge(field='post-private'), )),
        }))
        assert not matcher.do_aspects_match_filters(aspects, filters_=frozenset({
            filters.AnyLabel(labels=(labels.Value(field='post-id', value=123456),)),
            filters.NoLabels(labels=(labels.Badge(field='post-private'),)),
        }))

        assert matcher.do_aspects_match_filters(aspects, filters_=frozenset({
            filters.AnyLabel(labels=(labels.Value(field='post-id', value=123456), )),
            filters.AnyLabel(labels=(labels.Empty(field='post-stage'), )),
        }))
        assert not matcher.do_aspects_match_filters(aspects, filters_=frozenset({
            filters.AnyLabel(labels=(labels.Value(field='post-id', value=123456),)),
            filters.NoLabels(labels=(labels.Empty(field='post-stage'), )),
        }))

        assert matcher.do_aspects_match_filters(aspects, filters_=frozenset({
            filters.AnyLabel(labels=(labels.Value(field='post-id', value=123456), )),
            filters.AnyRange(ranges=(ranges.MoreThan(field='post-modified-at', value=0),)),
            filters.AnyRange(ranges=(ranges.MoreThan(field='post-published-at', value=0),)),
        }))
        assert not matcher.do_aspects_match_filters(aspects, filters_=frozenset({
            filters.AnyLabel(labels=(labels.Value(field='post-id', value=123456),)),
            filters.AnyRange(ranges=(ranges.MoreThan(field='post-modified-at', value=0),)),
            filters.NoRanges(ranges=(ranges.MoreThan(field='post-published-at', value=0),)),
        }))

        assert matcher.do_aspects_match_filters(aspects, filters_=frozenset({
            filters.AnyLabel(labels=(labels.Value(field='post-id', value=123456), )),
            filters.AnyRange(ranges=(ranges.MoreThan(field='post-modified-at', value=0),)),
            filters.AnyRange(ranges=(ranges.LessThan(field='post-published-at', value=week_ago),)),
        }))
        assert not matcher.do_aspects_match_filters(aspects, filters_=frozenset({
            filters.AnyLabel(labels=(labels.Value(field='post-id', value=123456),)),
            filters.AnyRange(ranges=(ranges.MoreThan(field='post-modified-at', value=0),)),
            filters.AnyRange(ranges=(ranges.LessThan(field='post-published-at', value=week_ago - Hours(1)),)),
        }))
        assert matcher.do_aspects_match_filters(aspects, filters_=frozenset({
            filters.AnyLabel(labels=(labels.Value(field='post-id', value=123456),)),
            filters.AnyRange(ranges=(ranges.MoreThan(field='post-modified-at', value=0),)),
            filters.AnyRange(ranges=(ranges.Between(field='post-published-at', min_value=week_ago - Hours(1), max_value=week_ago + Hours(2)),)),
        }))
        assert not matcher.do_aspects_match_filters(aspects, filters_=frozenset({
            filters.AnyLabel(labels=(labels.Value(field='post-id', value=123456),)),
            filters.AnyRange(ranges=(ranges.MoreThan(field='post-modified-at', value=0),)),
            filters.AnyRange(ranges=(ranges.Between(field='post-published-at', min_value=week_ago + Hours(1), max_value=week_ago + Hours(2)),)),
        }))
        assert matcher.do_aspects_match_filters(aspects, filters_=frozenset({
            filters.AnyLabel(labels=(labels.Value(field='post-id', value=123456),)),
            filters.AnyRange(ranges=(ranges.MoreThan(field='post-modified-at', value=week_ago - Hours(1)),)),
            filters.AnyRange(ranges=(ranges.Between(field='post-published-at', min_value=week_ago - Hours(1), max_value=week_ago + Hours(2)),)),
        }))

    class Aspects(Matcher.IAspects):
        @property
        def labels(self):
            return frozenset({
                labels.Value(field='post-id', value=123456),
                labels.Value(field='post-type', value='page'),
                labels.Value(field='post-status', value='published-to-site(promoted=false)'),
                labels.Badge(field='post-private'),
                labels.Value(field='post-primary-tag', value='tag-1'),
                labels.Value(field='post-regular-tag', value='tag-1'),
                labels.Value(field='post-regular-tag', value='tag-2'),
                labels.Value(field='post-primary-section', value=123),
                labels.Value(field='post-regular-section', value=123),
                labels.Value(field='post-regular-section', value=456),
                labels.Value(field='post-community', value=1234),
                labels.Value(field='post-author', value=2345),
                labels.Value(field='post-author', value=3456),
                labels.Empty(field='post-stage'),
            })

        @property
        def values(self):
            return frozenset({
                Value(field='post-modified-at', value=TestMarcher.NOW - Days(3)),
                Value(field='post-published-at', value=TestMarcher.NOW - Days(7)),
            })
