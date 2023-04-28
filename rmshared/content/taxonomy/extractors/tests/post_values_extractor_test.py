from rmshared.typings import read_only

from rmshared.content.taxonomy import core
from rmshared.content.taxonomy import graph
from rmshared.content.taxonomy import posts

from rmshared.content.taxonomy.extractors.values import PostValuesExtractor


class TestPostValuesExtractor:
    def test_it_should_extract_values(self):
        extractor_1 = PostValuesExtractor(graph.posts.Post(
            id=123,
            type=posts.consts.POST.TYPE.HOW_TO,
            status=posts.statuses.Published(scope=posts.published.scopes.Site(is_promoted=False)),
            stage_id=234,
            is_private=True,
            is_suspicious=True,
            is_excluded_from_search=True,
            modified_ts=1682679355,
            scheduled_ts=None,
            published_ts=1682679355,
            title='How to make a cake',
            subtitles=('Ingredients', 'Instructions', 'Tips'),
            bodies=('1. Mix the ingredients', '2. Bake the cake', '3. Enjoy!'),
            primary_tag=graph.others.Tag(slug='food'),
            regular_tags=frozenset({graph.others.Tag(slug='cake'), graph.others.Tag(slug='dessert')}),
            primary_section=graph.others.Section(id=345),
            regular_sections=frozenset({graph.others.Section(id=456), graph.others.Section(id=567)}),
            community=graph.others.Community(id=678, slug='food', title='Food', about_html='About food', description='Food is good'),
            authors=(
                graph.users.UserProfile(
                    id=789, user=graph.users.User(id=890, details=None), slug='jane-doe', title='Jane Doe', about_html='', description='', details=None
                ),
                graph.users.UserProfile(
                    id=901, user=graph.users.User(id=1234, details=None), slug='jane-smith', title='Jane Smith', about_html='', description='', details=None
                ),
            ),
            page_layout=graph.others.Layout(slug='How_To'),
            editor_layout=graph.others.Layout(slug='EE_How_To'),
            site_specific_info=read_only({'foo': {'bar': 'baz', 'qux': [123, 456], 'qxa': None}}),
        ))

        assert list(extractor_1.extract_values(core.fields.System('post-id'))) == [123]
        assert list(extractor_1.extract_values(core.fields.System('post-type'))) == ['how-to']
        assert list(extractor_1.extract_values(core.fields.System('post-status'))) == ['published-to-site(promoted=false)']
        assert list(extractor_1.extract_values(core.fields.System('post-stage'))) == [234]
        assert list(extractor_1.extract_values(core.fields.System('post-is-private'))) == [True]
        assert list(extractor_1.extract_values(core.fields.System('post-is-suspicious'))) == [True]
        assert list(extractor_1.extract_values(core.fields.System('post-is-excluded-from-search'))) == [True]
        assert list(extractor_1.extract_values(core.fields.System('post-modified-at'))) == [1682679355]
        assert list(extractor_1.extract_values(core.fields.System('post-scheduled-at'))) == []
        assert list(extractor_1.extract_values(core.fields.System('post-published-at'))) == [1682679355]
        assert list(extractor_1.extract_values(core.fields.System('post-title'))) == ['How to make a cake']
        assert list(extractor_1.extract_values(core.fields.System('post-subtitle'))) == ['Ingredients', 'Instructions', 'Tips']
        assert list(extractor_1.extract_values(core.fields.System('post-body'))) == ['1. Mix the ingredients', '2. Bake the cake', '3. Enjoy!']
        assert list(extractor_1.extract_values(core.fields.System('post-primary-tag'))) == ['food']
        assert list(extractor_1.extract_values(core.fields.System('post-regular-tag'))) == ['cake', 'dessert']
        assert list(extractor_1.extract_values(core.fields.System('post-primary-section'))) == [345]
        assert list(extractor_1.extract_values(core.fields.System('post-regular-section'))) == [456, 567]
        assert list(extractor_1.extract_values(core.fields.System('post-community'))) == [678]
        assert list(extractor_1.extract_values(core.fields.System('post-author'))) == [789, 901]
        assert list(extractor_1.extract_values(core.fields.System('post-page-layout'))) == ['How_To']
        assert list(extractor_1.extract_values(core.fields.System('post-editor-layout'))) == ['EE_How_To']
        assert list(extractor_1.extract_values(core.fields.Custom('post-site-specific-info', path='foo.bar'))) == ['baz']
        assert list(extractor_1.extract_values(core.fields.Custom('post-site-specific-info', path='foo.qux'))) == [123, 456]
        assert list(extractor_1.extract_values(core.fields.Custom('post-site-specific-info', path='foo.qxa'))) == []

        extractor_2 = PostValuesExtractor(graph.posts.Post(
            id=2345,
            type=posts.consts.POST.TYPE.PRODUCT,
            status=posts.statuses.Draft(stage=posts.drafts.stages.InProgress(is_rejected=True)),
            stage_id=None,
            is_private=False,
            is_suspicious=False,
            is_excluded_from_search=False,
            modified_ts=1682679355,
            scheduled_ts=1682765755,
            published_ts=None,
            title='',
            subtitles=tuple(),
            bodies=tuple(),
            primary_tag=None,
            regular_tags=frozenset(),
            primary_section=None,
            regular_sections=frozenset(),
            community=None,
            authors=tuple(),
            page_layout=None,
            editor_layout=None,
            site_specific_info=read_only(dict()),
        ))

        assert list(extractor_2.extract_values(core.fields.System('post-id'))) == [2345]
        assert list(extractor_2.extract_values(core.fields.System('post-type'))) == ['product']
        assert list(extractor_2.extract_values(core.fields.System('post-status'))) == ['draft-in-progress(rejected=true)']
        assert list(extractor_2.extract_values(core.fields.System('post-stage'))) == []
        assert list(extractor_2.extract_values(core.fields.System('post-is-private'))) == [False]
        assert list(extractor_2.extract_values(core.fields.System('post-is-suspicious'))) == [False]
        assert list(extractor_2.extract_values(core.fields.System('post-is-excluded-from-search'))) == [False]
        assert list(extractor_2.extract_values(core.fields.System('post-modified-at'))) == [1682679355]
        assert list(extractor_2.extract_values(core.fields.System('post-scheduled-at'))) == [1682765755]
        assert list(extractor_2.extract_values(core.fields.System('post-published-at'))) == []
        assert list(extractor_2.extract_values(core.fields.System('post-title'))) == ['']
        assert list(extractor_2.extract_values(core.fields.System('post-subtitle'))) == []
        assert list(extractor_2.extract_values(core.fields.System('post-body'))) == []
        assert list(extractor_2.extract_values(core.fields.System('post-primary-tag'))) == []
        assert list(extractor_2.extract_values(core.fields.System('post-regular-tag'))) == []
        assert list(extractor_2.extract_values(core.fields.System('post-primary-section'))) == []
        assert list(extractor_2.extract_values(core.fields.System('post-regular-section'))) == []
        assert list(extractor_2.extract_values(core.fields.System('post-community'))) == []
        assert list(extractor_2.extract_values(core.fields.System('post-author'))) == []
        assert list(extractor_2.extract_values(core.fields.System('post-page-layout'))) == []
        assert list(extractor_2.extract_values(core.fields.System('post-editor-layout'))) == []
        assert list(extractor_2.extract_values(core.fields.Custom('post-site-specific-info', path='foo.bar'))) == []
        assert list(extractor_2.extract_values(core.fields.Custom('post-site-specific-info', path='foo.qux'))) == []
        assert list(extractor_2.extract_values(core.fields.Custom('post-site-specific-info', path='foo.qxa'))) == []
