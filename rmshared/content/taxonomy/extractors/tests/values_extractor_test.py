from rmshared.typings import read_only

from rmshared.content.taxonomy import graph
from rmshared.content.taxonomy import posts
from rmshared.content.taxonomy import users

from rmshared.content.taxonomy.extractors.factory import Factory


class TestPostValuesExtractor:
    def test_it_should_extract_values_from_post(self):
        extractor_1 = Factory.make_values_extractor_for_post(graph.posts.Post(
            id=123,
            type=posts.consts.POST.TYPE.HOW_TO,
            status=posts.statuses.Published(scope=posts.published.scopes.Site(is_promoted=False)),
            stage_id=234,
            is_private=True,
            is_suspicious=True,
            is_excluded_from_search=True,
            modified_ts=1682679354,
            scheduled_ts=None,
            published_ts=1682679356,
            embargoed_until_ts=None,
            title='How to make a cake',
            subtitles=('Ingredients', 'Instructions', 'Tips'),
            bodies=('1. Mix the ingredients', '2. Bake the cake', '3. Enjoy!'),
            primary_tag=graph.others.Tag(slug='food'),
            regular_tags=frozenset({graph.others.Tag(slug='cake'), graph.others.Tag(slug='dessert')}),
            primary_section=graph.sections.Section(id=345),
            regular_sections=frozenset({graph.sections.Section(id=456), graph.sections.Section(id=567)}),
            community=graph.others.Community(id=678, slug='food', title='Food', about_html='About food', description='Food is good', details=None),
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
            lifetime_page_views_count=123456,
        ))

        assert list(extractor_1.extract_values(posts.fields.Id())) == [123]
        assert list(extractor_1.extract_values(posts.fields.Type())) == ['how-to']
        assert list(extractor_1.extract_values(posts.fields.Status())) == ['published-to-site(promoted=false)']
        assert list(extractor_1.extract_values(posts.fields.Stage())) == [234]
        assert list(extractor_1.extract_values(posts.fields.IsPrivate())) == [True]
        assert list(extractor_1.extract_values(posts.fields.IsSuspicious())) == [True]
        assert list(extractor_1.extract_values(posts.fields.IsExcludedFromSearch())) == [True]
        assert list(extractor_1.extract_values(posts.fields.ModifiedAt())) == [1682679354]
        assert list(extractor_1.extract_values(posts.fields.ScheduledAt())) == []
        assert list(extractor_1.extract_values(posts.fields.PublishedAt())) == [1682679356]
        assert list(extractor_1.extract_values(posts.fields.EmbargoedUntil())) == []
        assert list(extractor_1.extract_values(posts.fields.Title())) == ['How to make a cake']
        assert list(extractor_1.extract_values(posts.fields.Subtitle())) == ['Ingredients', 'Instructions', 'Tips']
        assert list(extractor_1.extract_values(posts.fields.Body())) == ['1. Mix the ingredients', '2. Bake the cake', '3. Enjoy!']
        assert list(extractor_1.extract_values(posts.fields.PrimaryTag())) == ['food']
        assert list(extractor_1.extract_values(posts.fields.RegularTag())) == ['cake', 'dessert']
        assert list(extractor_1.extract_values(posts.fields.PrimarySection())) == [345]
        assert list(extractor_1.extract_values(posts.fields.RegularSection())) == [456, 567]
        assert list(extractor_1.extract_values(posts.fields.Community())) == [678]
        assert list(extractor_1.extract_values(posts.fields.Author())) == [789, 901]
        assert list(extractor_1.extract_values(posts.fields.PageLayout())) == ['How_To']
        assert list(extractor_1.extract_values(posts.fields.EditorLayout())) == ['EE_How_To']
        assert list(extractor_1.extract_values(posts.fields.CustomField(path='foo.bar'))) == ['baz']
        assert list(extractor_1.extract_values(posts.fields.CustomField(path='foo.qux'))) == [123, 456]
        assert list(extractor_1.extract_values(posts.fields.CustomField(path='foo.qxa'))) == []
        assert list(extractor_1.extract_values(posts.fields.PageViewsCount())) == [123456]

        extractor_2 = Factory.make_values_extractor_for_post(graph.posts.Post(
            id=2345,
            type=posts.consts.POST.TYPE.PRODUCT,
            status=posts.statuses.Draft(stage=posts.drafts.stages.InProgress(is_rejected=True)),
            stage_id=None,
            is_private=False,
            is_suspicious=False,
            is_excluded_from_search=False,
            modified_ts=1682679354,
            scheduled_ts=1682765755,
            published_ts=None,
            embargoed_until_ts=1682765756,
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
            lifetime_page_views_count=0,
        ))

        assert list(extractor_2.extract_values(posts.fields.Id())) == [2345]
        assert list(extractor_2.extract_values(posts.fields.Type())) == ['product']
        assert list(extractor_2.extract_values(posts.fields.Status())) == ['draft-in-progress(rejected=true)']
        assert list(extractor_2.extract_values(posts.fields.Stage())) == []
        assert list(extractor_2.extract_values(posts.fields.IsPrivate())) == [False]
        assert list(extractor_2.extract_values(posts.fields.IsSuspicious())) == [False]
        assert list(extractor_2.extract_values(posts.fields.IsExcludedFromSearch())) == [False]
        assert list(extractor_2.extract_values(posts.fields.ModifiedAt())) == [1682679354]
        assert list(extractor_2.extract_values(posts.fields.ScheduledAt())) == [1682765755]
        assert list(extractor_2.extract_values(posts.fields.PublishedAt())) == []
        assert list(extractor_2.extract_values(posts.fields.EmbargoedUntil())) == [1682765756]
        assert list(extractor_2.extract_values(posts.fields.Title())) == ['']
        assert list(extractor_2.extract_values(posts.fields.Subtitle())) == []
        assert list(extractor_2.extract_values(posts.fields.Body())) == []
        assert list(extractor_2.extract_values(posts.fields.PrimaryTag())) == []
        assert list(extractor_2.extract_values(posts.fields.RegularTag())) == []
        assert list(extractor_2.extract_values(posts.fields.PrimarySection())) == []
        assert list(extractor_2.extract_values(posts.fields.RegularSection())) == []
        assert list(extractor_2.extract_values(posts.fields.Community())) == []
        assert list(extractor_2.extract_values(posts.fields.Author())) == []
        assert list(extractor_2.extract_values(posts.fields.PageLayout())) == []
        assert list(extractor_2.extract_values(posts.fields.EditorLayout())) == []
        assert list(extractor_2.extract_values(posts.fields.CustomField(path='foo.bar'))) == []
        assert list(extractor_2.extract_values(posts.fields.CustomField(path='foo.qux'))) == []
        assert list(extractor_2.extract_values(posts.fields.CustomField(path='foo.qxa'))) == []
        assert list(extractor_2.extract_values(posts.fields.PageViewsCount())) == [0]

    def test_it_should_extract_values_from_user_profiles(self):
        extractor_1 = Factory.make_values_extractor_for_user_profile(graph.users.UserProfile(
            id=777,
            user=graph.users.User(
                id=8765,
                details=graph.users.UserDetails(
                    status=users.consts.USER.STATUS.ACTIVE,
                    emails=frozenset({'email_1@example.org', 'email_2@example.org'}),
                    groups=frozenset({
                        graph.users.UserGroup(slug='user-group-1'),
                        graph.users.UserGroup(slug='user-group-2'),
                    }),
                    communities=frozenset({
                        graph.others.Community(
                            id=987,
                            slug='community-1',
                            title='Community #1',
                            about_html='About community #1',
                            description='Description of community #1',
                            details=None,
                        ),
                        graph.others.Community(
                            id=876,
                            slug='community-2',
                            title='Community #2',
                            about_html='About community #2',
                            description='Description of community #2',
                            details=None,
                        ),
                    }),
                    access_roles=frozenset({
                        graph.users.AccessRole(id=12345),
                        graph.users.AccessRole(id=54321),
                    }),
                    last_login_ts=1440000000,
                ),
            ),
            slug='user-1',
            title='User #1',
            about_html='About user #1',
            description='Description of user #1',
            details=graph.users.UserProfileDetails(
                status=users.statuses.Inactive(is_banned=True),
                site_specific_info=read_only({'foo': {'bar': 'baz', 'qux': [123, 456], 'qxa': None}}),
                lifetime_posts_count=54321,
            )
        ))

        assert list(extractor_1.extract_values(users.fields.Id())) == [777]
        assert list(extractor_1.extract_values(users.fields.Slug())) == ['user-1']
        assert list(extractor_1.extract_values(users.fields.Title())) == ['User #1']
        assert list(extractor_1.extract_values(users.fields.Owner())) == [8765]
        assert list(extractor_1.extract_values(users.fields.Status())) == ['inactive(banned=true)']
        assert list(extractor_1.extract_values(users.fields.AboutHtml())) == ['About user #1']
        assert list(extractor_1.extract_values(users.fields.Description())) == ['Description of user #1']
        assert frozenset(extractor_1.extract_values(users.fields.Email())) == frozenset({'email_1@example.org', 'email_2@example.org'})
        assert frozenset(extractor_1.extract_values(users.fields.Group())) == frozenset({'user-group-1', 'user-group-2'})
        assert frozenset(extractor_1.extract_values(users.fields.Community())) == frozenset({987, 876})
        assert frozenset(extractor_1.extract_values(users.fields.AccessRole())) == frozenset({12345, 54321})
        assert list(extractor_1.extract_values(users.fields.LastLoggedInAt())) == [1440000000]
        assert list(extractor_1.extract_values(users.fields.CustomField(path='foo.bar'))) == ['baz']
        assert list(extractor_1.extract_values(users.fields.CustomField(path='foo.qux'))) == [123, 456]
        assert list(extractor_1.extract_values(users.fields.CustomField(path='foo.qxa'))) == []
        assert list(extractor_1.extract_values(users.fields.PostsCount())) == [54321]
