from pytest import fixture

from rmshared.typings import read_only
from rmshared.units import Days

from rmshared.content.taxonomy import posts
from rmshared.content.taxonomy import users
from rmshared.content.taxonomy import filters
from rmshared.content.taxonomy.abc import Aspects
from rmshared.content.taxonomy.abc import Range
from rmshared.content.taxonomy.abc import Value
from rmshared.content.taxonomy.matcher import Matcher


class TestMarcher:
    NOW = 1440000000

    @fixture
    def matcher(self) -> Matcher:
        return Matcher()

    def test_it_should_check_id_post_aspects_match_filters(self, matcher: Matcher):
        assert matcher.do_aspects_match_filters(self.POST_ASPECTS, filters_=frozenset({
            filters.AnyLabel(labels=(posts.labels.Id(value=123456), users.labels.Id(value=123456))),
        }))
        assert not matcher.do_aspects_match_filters(self.POST_ASPECTS, filters_=frozenset({
            filters.NoLabels(labels=(posts.labels.Id(value=123456), )),
        }))
        assert matcher.do_aspects_match_filters(self.POST_ASPECTS, filters_=frozenset({
            filters.AnyLabel(labels=(posts.labels.Id(value=123456), )),
            filters.AnyLabel(labels=tuple(map(posts.labels.Type, posts.consts.POST.TYPE.ALL)))
        }))
        assert not matcher.do_aspects_match_filters(self.POST_ASPECTS, filters_=frozenset({
            filters.AnyLabel(labels=(posts.labels.Id(value=123456),)),
            filters.AnyLabel(labels=tuple(map(posts.labels.Type, posts.consts.POST.TYPE.ALL - {posts.consts.POST.TYPE.PAGE})))
        }))
        assert not matcher.do_aspects_match_filters(self.POST_ASPECTS, filters_=frozenset({
            filters.AnyLabel(labels=(posts.labels.Id(value=123456),)),
            filters.NoLabels(labels=(posts.labels.Type(type=posts.consts.POST.TYPE.PAGE),))
        }))
        assert not matcher.do_aspects_match_filters(self.POST_ASPECTS, filters_=frozenset({
            filters.NoLabels(labels=(posts.labels.Id(value=123456),)),
            filters.AnyLabel(labels=(posts.labels.Type(type=posts.consts.POST.TYPE.PAGE),))
        }))
        assert matcher.do_aspects_match_filters(self.POST_ASPECTS, filters_=frozenset({
            filters.AnyLabel(labels=(posts.labels.Id(value=123456),)),
            filters.AnyLabel(labels=(posts.labels.Private(),))
        }))
        assert not matcher.do_aspects_match_filters(self.POST_ASPECTS, filters_=frozenset({
            filters.AnyLabel(labels=(posts.labels.Id(value=123456),)),
            filters.AnyLabel(labels=(posts.labels.Suspicious(),))
        }))
        assert matcher.do_aspects_match_filters(self.POST_ASPECTS, filters_=frozenset({
            filters.AnyLabel(labels=(posts.labels.Id(value=123456),)),
            filters.AnyLabel(labels=(posts.labels.NoStages(),))
        }))
        assert not matcher.do_aspects_match_filters(self.POST_ASPECTS, filters_=frozenset({
            filters.AnyLabel(labels=(posts.labels.Id(value=123456),)),
            filters.AnyLabel(labels=(posts.labels.Stage(id=987654321),))
        }))
        assert matcher.do_aspects_match_filters(self.POST_ASPECTS, filters_=frozenset({
            filters.AnyLabel(labels=(posts.labels.Id(value=123456),)),
            filters.AnyRange(ranges=(
                Range(field=posts.fields.ModifiedAt(), min_value=None, max_value=None),
            )),
        }))
        assert matcher.do_aspects_match_filters(self.POST_ASPECTS, filters_=frozenset({
            filters.AnyLabel(labels=(posts.labels.Id(value=123456),)),
            filters.AnyRange(ranges=(
                Range(field=posts.fields.ModifiedAt(), min_value=self.NOW - Days(7), max_value=self.NOW),
            )),
        }))
        assert matcher.do_aspects_match_filters(self.POST_ASPECTS, filters_=frozenset({
            filters.AnyLabel(labels=(posts.labels.Id(value=123456),)),
            filters.AnyRange(ranges=(
                Range(field=posts.fields.ModifiedAt(), min_value=self.NOW - Days(7), max_value=self.NOW),
                Range(field=posts.fields.PublishedAt(), min_value=self.NOW - Days(7), max_value=self.NOW),
            )),
        }))
        assert matcher.do_aspects_match_filters(self.POST_ASPECTS, filters_=frozenset({
            filters.AnyLabel(labels=(posts.labels.Id(value=123456),)),
            filters.NoRanges(ranges=(
                Range(field=posts.fields.ModifiedAt(), min_value=None, max_value=self.NOW - Days(7) - 1),
                Range(field=posts.fields.ModifiedAt(), min_value=self.NOW - Days(7) + 1, max_value=None),
                Range(field=posts.fields.PublishedAt(), min_value=None, max_value=self.NOW - Days(14) - 1),
                Range(field=posts.fields.PublishedAt(), min_value=self.NOW - Days(14) + 1, max_value=None),
            )),
        }))
        assert not matcher.do_aspects_match_filters(self.POST_ASPECTS, filters_=frozenset({
            filters.AnyLabel(labels=(posts.labels.Id(value=123456),)),
            filters.AnyRange(ranges=(
                Range(field=posts.fields.ModifiedAt(), min_value=None, max_value=self.NOW - Days(7) - 1),
                Range(field=posts.fields.ModifiedAt(), min_value=self.NOW - Days(7) + 1, max_value=None),
                Range(field=posts.fields.PublishedAt(), min_value=None, max_value=self.NOW - Days(14) - 1),
                Range(field=posts.fields.PublishedAt(), min_value=self.NOW - Days(14) + 1, max_value=None),
            )),
        }))
        assert not matcher.do_aspects_match_filters(self.POST_ASPECTS, filters_=frozenset({
            filters.AnyLabel(labels=(posts.labels.Id(value=123456),)),
            filters.AnyRange(ranges=(
                Range(field=posts.fields.ScheduledAt(), min_value=None, max_value=None),
            )),
        }))

    POST_ASPECTS = Aspects(
        texts=frozenset(),
        labels=frozenset({
            posts.labels.Id(value=123456),
            posts.labels.Type(type=posts.consts.POST.TYPE.PAGE),
            posts.labels.Status(status=posts.statuses.Published(scope=posts.published.scopes.Site(is_promoted=False))),
            posts.labels.Private(),
            posts.labels.PrimaryTag(slug='tag-1'),
            posts.labels.RegularTag(slug='tag-2'),
            posts.labels.RegularTag(slug='tag-3'),
            posts.labels.PrimarySection(id=123),
            posts.labels.RegularSection(id=456),
            posts.labels.RegularSection(id=789),
            posts.labels.Community(id=1234),
            posts.labels.Author(id=2345),
            posts.labels.Author(id=3456),
            posts.labels.NoStages(),
        }),
        values=frozenset({
            Value(field=posts.fields.ModifiedAt(), value=NOW - Days(7)),
            Value(field=posts.fields.PublishedAt(), value=NOW - Days(14)),
        }),
        extras=read_only(dict()),
    )
