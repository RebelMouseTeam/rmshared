from rmshared.typings import read_only

from rmshared.content.taxonomy import posts
from rmshared.content.taxonomy import users
from rmshared.content.taxonomy import sections

from rmshared.content.taxonomy.graph.posts import Post
from rmshared.content.taxonomy.graph.users import User
from rmshared.content.taxonomy.graph.users import UserGroup
from rmshared.content.taxonomy.graph.users import UserDetails
from rmshared.content.taxonomy.graph.users import UserProfile
from rmshared.content.taxonomy.graph.users import UserProfileDetails
from rmshared.content.taxonomy.graph.users import AccessRole
from rmshared.content.taxonomy.graph.sections import Section
from rmshared.content.taxonomy.graph.sections import SectionAccess
from rmshared.content.taxonomy.graph.sections import SectionDetails
from rmshared.content.taxonomy.graph.sections import SectionMetaInfo
from rmshared.content.taxonomy.graph.sections import SectionSettings
from rmshared.content.taxonomy.graph.others import Tag
from rmshared.content.taxonomy.graph.others import Image
from rmshared.content.taxonomy.graph.others import Layout
from rmshared.content.taxonomy.graph.others import Community


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
    primary_tag=Tag(slug='tag-1'),
    regular_tags=frozenset({
        Tag(slug='tag-1'),
        Tag(slug='tag-2'),
    }),
    primary_section=Section(id=123, details=None),
    regular_sections=frozenset({
        Section(id=123, details=None),
        Section(id=234, details=None),
    }),
    community=Community(
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
    page_layout=Layout(slug='layout-1'),
    editor_layout=Layout(slug='layout-2'),
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
    'primary_section': {'id': 123, 'details': None},
    'regular_sections': [
        {'id': 123, 'details': None},
        {'id': 234, 'details': None},
    ],
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
        Tag(slug='tag-1'),
        Tag(slug='tag-2'),
    }),
    primary_section=None,
    regular_sections=frozenset({
        Section(id=123, details=None),
        Section(id=234, details=None),
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
    'regular_sections': [
        {'id': 123, 'details': None},
        {'id': 234, 'details': None},
    ],
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

SECTION_1 = Section(
    id=123,
    details=SectionDetails(
        path='path/to/section-1',
        slug='section-1',
        title='Section #1',
        order_id=1,
        created_ts=1440000000.0,
        is_read_only=False,
        ancestors=(
            Section(id=234, details=None),
            Section(id=345, details=None),
        ),
        visibility=sections.consts.VISIBILITY.STATUS.LISTED,
        access=SectionAccess(read_access_kind=sections.access.Public()),
        settings=SectionSettings(
            open_in_new_tab=True,
            allow_community_posts=True,
            hide_from_entry_editor=False,
            lock_posts_after_publishing=False,
        ),
        meta_info=SectionMetaInfo(
            image=Image(id=123),
            link_out='https://example.org',
            meta_tags=('tag-1', 'tag-2'),
            meta_title='Meta title',
            about_html='About section #1',
        ),
        site_specific_info=read_only({'some': {'info': 'here'}}),
    ),
)

SECTION_1_DATA = {
    'id': 123,
    'details': {
        'path': 'path/to/section-1',
        'slug': 'section-1',
        'title': 'Section #1',
        'order_id': 1,
        'created_ts': 1440000000,
        'is_read_only': False,
        'ancestors': [
            {'id': 234, 'details': None},
            {'id': 345, 'details': None},
        ],
        'visibility': {'listed': {}},
        'access': {'read_access_kind': {'public': {}}},
        'settings': {
            'open_in_new_tab': True,
            'allow_community_posts': True,
            'hide_from_entry_editor': False,
            'lock_posts_after_publishing': False,
        },
        'meta_info': {
            'image': {'id': 123},
            'link_out': 'https://example.org',
            'meta_tags': ['tag-1', 'tag-2'],
            'meta_title': 'Meta title',
            'about_html': 'About section #1',
        },
        'site_specific_info': {'some': {'info': 'here'}},
    },
}

SECTION_2 = Section(
    id=234,
    details=SectionDetails(
        path='section-2',
        slug='section-2',
        title='Section #2',
        order_id=2,
        created_ts=1440000000.0,
        is_read_only=True,
        ancestors=tuple(),
        visibility=sections.consts.VISIBILITY.STATUS.PRIVATE,
        access=SectionAccess(read_access_kind=sections.access.Restricted(is_inherited=True)),
        settings=SectionSettings(
            open_in_new_tab=False,
            allow_community_posts=False,
            hide_from_entry_editor=True,
            lock_posts_after_publishing=True,
        ),
        meta_info=SectionMetaInfo(
            image=None,
            link_out=None,
            meta_tags=(),
            meta_title='',
            about_html='',
        ),
        site_specific_info=read_only({}),
    ),
)

SECTION_2_DATA = {
    'id': 234,
    'details': {
        'path': 'section-2',
        'slug': 'section-2',
        'title': 'Section #2',
        'order_id': 2,
        'created_ts': 1440000000,
        'is_read_only': True,
        'ancestors': [],
        'visibility': {'private': {}},
        'access': {'read_access_kind': {'restricted': {'is_inherited': True}}},
        'settings': {
            'open_in_new_tab': False,
            'allow_community_posts': False,
            'hide_from_entry_editor': True,
            'lock_posts_after_publishing': True,
        },
        'meta_info': {
            'image': None,
            'link_out': None,
            'meta_tags': [],
            'meta_title': '',
            'about_html': '',
        },
        'site_specific_info': {},
    },
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
                Community(
                    id=987,
                    slug='community-1',
                    title='Community #1',
                    about_html='About community #1',
                    description='Description of community #1',
                    details=None,
                ),
                Community(
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
                    'id': 876,
                    'slug': 'community-2',
                    'title': 'Community #2',
                    'about_html': 'About community #2',
                    'description': 'Description of community #2',
                    'details': None,
                },
                {
                    'id': 987,
                    'slug': 'community-1',
                    'title': 'Community #1',
                    'about_html': 'About community #1',
                    'description': 'Description of community #1',
                    'details': None,
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
        'lifetime_posts_count': 54321,
    },
}
