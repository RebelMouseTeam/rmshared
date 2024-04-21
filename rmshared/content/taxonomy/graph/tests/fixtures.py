from rmshared.typings import read_only

from rmshared.content.taxonomy import posts
from rmshared.content.taxonomy import users

from rmshared.content.taxonomy.graph import others
from rmshared.content.taxonomy.graph.posts import Post
from rmshared.content.taxonomy.graph.users import User
from rmshared.content.taxonomy.graph.users import UserGroup
from rmshared.content.taxonomy.graph.users import UserDetails
from rmshared.content.taxonomy.graph.users import UserProfile
from rmshared.content.taxonomy.graph.users import UserProfileDetails
from rmshared.content.taxonomy.graph.users import AccessRole
from rmshared.content.taxonomy.graph.sections import Section


POST_1 = Post(
    id=777,
    type=posts.consts.POST.TYPE.PAGE,
    status=posts.statuses.Published(scope=posts.published.scopes.Site(is_promoted=False)),
    stage_id=12,
    is_private=False,
    is_suspicious=True,
    is_excluded_from_search=False,
    modified_ts=1440000000 - 100,
    scheduled_ts=1440000000 + 100,
    published_ts=None,
    embargoed_until_ts=1440000000,
    title='Article #1',
    subtitles=('Subtitle #1', 'Subtitle #2'),
    bodies=('Body #1', 'Body #2'),
    primary_tag=others.Tag(slug='tag-1'),
    regular_tags=frozenset({
        others.Tag(slug='tag-1'),
        others.Tag(slug='tag-2'),
    }),
    primary_section=Section(id=123),
    regular_sections=frozenset({
        Section(id=123),
        Section(id=234),
    }),
    community=others.Community(
        id=987,
        slug='community-1',
        title='Community #1',
        about_html='About community #1',
        description='Description of community #1',
        details=None,
    ),
    authors=(
        UserProfile(
            id=876,
            user=User(
                id=8765,
                details=None,
            ),
            slug='author-1',
            title='Author #1',
            about_html='About author #1',
            description='Description of author #1',
            details=None,
        ),
        UserProfile(
            id=765,
            user=User(
                id=7654,
                details=None,
            ),
            slug='author-2',
            title='Author #2',
            about_html='About author #2',
            description='Description of author #2',
            details=None,
        ),
    ),
    page_layout=others.Layout(slug='layout-1'),
    editor_layout=others.Layout(slug='layout-2'),
    site_specific_info=read_only({'some': {'info': 'here'}}),
    lifetime_page_views_count=54321,
)

POST_1_DATA = {
    'id': 777,
    'type': {'page': {}},
    'status': {'published': {'scope': {'site': {'is_promoted': False}}}},
    'stage_id': 12,
    'is_private': False,
    'is_suspicious': True,
    'is_excluded_from_search': False,
    'modified_ts': 1440000000 - 100,
    'scheduled_ts': 1440000000 + 100,
    'published_ts': None,
    'embargoed_until_ts': 1440000000,
    'title': 'Article #1',
    'subtitles': ['Subtitle #1', 'Subtitle #2'],
    'bodies': ['Body #1', 'Body #2'],
    'primary_tag': {'slug': 'tag-1'},
    'regular_tags': [{'slug': 'tag-1'}, {'slug': 'tag-2'}],
    'primary_section': {'id': 123},
    'regular_sections': [{'id': 123}, {'id': 234}],
    'community': {
        'id': 987,
        'slug': 'community-1',
        'title': 'Community #1',
        'about_html': 'About community #1',
        'description': 'Description of community #1',
        'details': None,
    },
    'authors': [
        {
            'id': 876,
            'user': {'id': 8765, 'details': None},
            'slug': 'author-1',
            'title': 'Author #1',
            'about_html': 'About author #1',
            'description': 'Description of author #1',
            'details': None,
        },
        {
            'id': 765,
            'user': {'id': 7654, 'details': None},
            'slug': 'author-2',
            'title': 'Author #2',
            'about_html': 'About author #2',
            'description': 'Description of author #2',
            'details': None,
        },
    ],
    'page_layout': {'slug': 'layout-1'},
    'editor_layout': {'slug': 'layout-2'},
    'site_specific_info': {'some': {'info': 'here'}},
    'lifetime_page_views_count': 54321,
}

POST_2 = Post(
    id=888,
    type=posts.consts.POST.TYPE.EVENT,
    status=posts.statuses.Draft(stage=posts.drafts.stages.InProgress(is_rejected=True)),
    stage_id=None,
    is_private=True,
    is_suspicious=False,
    is_excluded_from_search=False,
    modified_ts=1440000000 - 100,
    scheduled_ts=None,
    published_ts=1440000000,
    embargoed_until_ts=None,
    title='Article #2',
    subtitles=('Subtitle #1', 'Subtitle #2'),
    bodies=('Body #1', 'Body #2'),
    primary_tag=None,
    regular_tags=frozenset({
        others.Tag(slug='tag-1'),
        others.Tag(slug='tag-2'),
    }),
    primary_section=None,
    regular_sections=frozenset({
        Section(id=123),
        Section(id=234),
    }),
    community=None,
    authors=(
        UserProfile(
            id=876,
            user=User(
                id=8765,
                details=None,
            ),
            slug='author-1',
            title='Author #1',
            about_html='About author #1',
            description='Description of author #1',
            details=None,
        ),
    ),
    page_layout=None,
    editor_layout=None,
    site_specific_info=read_only({'some': {'info': 'here'}}),
    lifetime_page_views_count=54321,
)

POST_2_DATA = {
    'id': 888,
    'type': {'event': {}},
    'status': {'draft': {'stage': {'in-progress': {'is_rejected': True}}}},
    'stage_id': None,
    'is_private': True,
    'is_suspicious': False,
    'is_excluded_from_search': False,
    'modified_ts': 1440000000 - 100,
    'scheduled_ts': None,
    'published_ts': 1440000000,
    'embargoed_until_ts': None,
    'title': 'Article #2',
    'subtitles': ['Subtitle #1', 'Subtitle #2'],
    'bodies': ['Body #1', 'Body #2'],
    'primary_tag': None,
    'regular_tags': [{'slug': 'tag-1'}, {'slug': 'tag-2'}],
    'primary_section': None,
    'regular_sections': [{'id': 123}, {'id': 234}],
    'community': None,
    'authors': [
        {
            'id': 876,
            'user': {'id': 8765, 'details': None},
            'slug': 'author-1',
            'title': 'Author #1',
            'about_html': 'About author #1',
            'description': 'Description of author #1',
            'details': None,
        },
    ],
    'page_layout': None,
    'editor_layout': None,
    'site_specific_info': {'some': {'info': 'here'}},
    'lifetime_page_views_count': 54321,
}

USER_PROFILE_1 = UserProfile(
    id=777,
    user=User(
        id=8765,
        details=UserDetails(
            status=users.consts.USER.STATUS.ACTIVE,
            emails=frozenset({'email_1@example.org', 'email_2@example.org'}),
            groups=frozenset({
                UserGroup(slug='user-group-1'),
                UserGroup(slug='user-group-2'),
            }),
            communities=frozenset({
                others.Community(
                    id=987,
                    slug='community-1',
                    title='Community #1',
                    about_html='About community #1',
                    description='Description of community #1',
                    details=None,
                ),
                others.Community(
                    id=876,
                    slug='community-2',
                    title='Community #2',
                    about_html='About community #2',
                    description='Description of community #2',
                    details=None,
                ),
            }),
            access_roles=frozenset({
                AccessRole(id=12345),
                AccessRole(id=54321),
            }),
            last_login_ts=1440000000,
        ),
    ),
    slug='user-1',
    title='User #1',
    about_html='About user #1',
    description='Description of user #1',
    details=UserProfileDetails(
        status=users.statuses.Inactive(is_banned=True),
        site_specific_info=read_only({'some': {'info': 'here'}}),
        lifetime_posts_count=54321,
    ),
)

USER_PROFILE_1_DATA = {
    'id': 777,
    'user': {
        'id': 8765,
        'details': {
            'status': {'active': {}},
            'emails': ['email_1@example.org', 'email_2@example.org'],
            'groups': [
                {'slug': 'user-group-1'},
                {'slug': 'user-group-2'},
            ],
            'communities': [
                {
                    'id': 987,
                    'slug': 'community-1',
                    'title': 'Community #1',
                    'about_html': 'About community #1',
                    'description': 'Description of community #1',
                },
                {
                    'id': 876,
                    'slug': 'community-2',
                    'title': 'Community #2',
                    'about_html': 'About community #2',
                    'description': 'Description of community #2',
                },
            ],
            'access_roles': [
                {'id': 12345},
                {'id': 54321},
            ],
            'last_login_ts': 1440000000,
        },
    },
    'slug': 'user-1',
    'title': 'User #1',
    'about_html': 'About user #1',
    'description': 'Description of user #1',
    'details': {
        'status': {'inactive': {'is_banned': True}},
        'site_specific_info': {'some': {'info': 'here'}},
        'lifetime_posts_count': '54321',
    },
}
