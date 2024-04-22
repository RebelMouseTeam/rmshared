from collections import OrderedDict
from dataclasses import replace
from itertools import chain
from typing import Iterator
from typing import Mapping
from typing import Optional
from typing import Type

from faker import Faker
from faker import Generator
from faker.providers import internet
from faker.providers import lorem
from faker.providers import python
from faker.providers import BaseProvider

from rmshared import faker_ext
from rmshared.units import Hours
from rmshared.typings import read_only

from rmshared.content.taxonomy import graph
from rmshared.content.taxonomy import posts
from rmshared.content.taxonomy import users
from rmshared.content.taxonomy import sections

FakerWithProviders = Faker | Generator | BaseProvider | python.Provider | lorem.Provider | internet.Provider | faker_ext.Provider


class Fakes:
    NOW = 1440000000
    SEED = 1231

    def __init__(self, now=NOW, seed=SEED):
        self.now = now
        self.faker: FakerWithProviders = Faker()
        self.faker.add_provider(faker_ext.Provider)
        self.faker.seed_instance(seed)
        self.posts = posts.Fakes(now, seed)
        self.users = users.Fakes(now, seed)
        self.sections = sections.Fakes(now, seed)

    def make_post(self, post_id: Optional[int] = None) -> graph.posts.Post:
        status = self.make_post_status_other_than(posts.statuses.Removed)
        primary_tag_or_none = self.faker.random_element(elements=(None, self.make_tag()))
        primary_section_or_none = self.faker.random_element(elements=(None, self.make_section()))

        modified_ts = self.now - Hours(self.faker.random_int(min=0, max=48))

        if isinstance(status, posts.statuses.Draft):
            scheduled_ts = self.now + Hours(self.faker.random_int(min=0, max=48))
            scheduled_ts_or_none = self.faker.random_element(elements=OrderedDict([(None, 0.85), (scheduled_ts, 0.15)]))
            published_ts_or_none = None
            embargoed_until_ts_or_none = self.faker.random_element(elements=OrderedDict([(None, 0.95), (self.now + Hours(1), 0.05)]))
        else:
            published_ts_or_none = self.now - Hours(self.faker.random_int(min=0, max=48))
            scheduled_ts_or_none = None
            embargoed_until_ts_or_none = None

        return graph.posts.Post(
            id=post_id or self.faker.random_int(max=99999999),
            type=self.faker.random_element(elements=posts.consts.POST.TYPE.ALL),
            status=status,
            stage_id=self.faker.random_element(elements=(None, self.faker.random_int(max=20))),
            is_private=self.faker.random_element(elements=OrderedDict([(True, 0.01), (False, 0.99)])),
            is_suspicious=self.faker.random_element(elements=OrderedDict([(True, 0.01), (False, 0.99)])),
            is_excluded_from_search=self.faker.random_element(elements=OrderedDict([(True, 0.05), (False, 0.95)])),
            modified_ts=modified_ts,
            scheduled_ts=scheduled_ts_or_none,
            published_ts=published_ts_or_none,
            embargoed_until_ts=embargoed_until_ts_or_none,
            title=self.faker.sentence(),
            subtitles=tuple(self.faker.stream_random_items(self.faker.sentence, max_size=5)),
            bodies=tuple(self.faker.stream_random_items(self.faker.text, max_size=5)),
            primary_tag=primary_tag_or_none,
            regular_tags=frozenset(self._stream_tags(primary_tag_or_none)),
            primary_section=primary_section_or_none,
            regular_sections=frozenset(self._stream_sections(primary_section_or_none)),
            community=self.faker.random_element(elements=(None, self._make_community_without_details())),
            authors=tuple(self.faker.stream_random_items(self._make_user_profile_without_details, max_size=5, min_size=1)),
            page_layout=self.faker.random_element(elements=(None, self._make_layout_without_details())),
            editor_layout=self.faker.random_element(elements=(None, self._make_layout_without_details())),
            site_specific_info=self._make_site_specific_info(),
            lifetime_page_views_count=self.faker.random_int(max=99999),
        )

    def make_post_status(self) -> posts.statuses.Status:
        return self.posts.make_status()

    def make_post_status_other_than(self, status_type: Type[posts.statuses.Status]) -> posts.statuses.Status:
        return self.posts.make_status_other_than(status_types={status_type})

    def make_draft_post_stage(self) -> posts.drafts.stages.Stage:
        return self.posts.make_draft_stage()

    def make_published_post_scope(self) -> posts.published.scopes.Scope:
        return self.posts.make_published_scope()

    def _stream_tags(self, primary_tag: Optional[graph.others.Tag] = None) -> Iterator[graph.others.Tag]:
        return chain(filter(None, [primary_tag]), self.faker.stream_random_items(self.make_tag, max_size=5))

    def make_tag(self) -> graph.others.Tag:
        return graph.others.Tag(slug=self.faker.slug())

    def _stream_sections(self, primary_section: Optional[graph.sections.Section] = None) -> Iterator[graph.sections.Section]:
        return chain(filter(None, [primary_section]), self.faker.stream_random_items(self.make_section, max_size=5))

    def make_section(self, section_id: Optional[int] = None) -> graph.sections.Section:
        section = self._make_section_without_details(section_id)
        section = replace(section, details=self._make_section_details())
        return section

    def _make_section_without_details(self, section_id: Optional[int] = None) -> graph.sections.Section:
        return graph.sections.Section(id=section_id or self.faker.random_int(max=999999), details=None)

    def _make_section_details(self) -> graph.sections.SectionDetails:
        return graph.sections.SectionDetails(
            path=self.faker.uri_path(),
            slug=self.faker.slug(),
            title=self.faker.sentence(),
            order_id=self.faker.random_int(max=999),
            created_ts=self.faker.random_int(max=self.now),
            is_read_only=self.faker.random_element(elements=OrderedDict([(True, 0.01), (False, 0.99)])),
            ancestors=tuple(self.faker.stream_random_items(self._make_section_without_details, max_size=5)),
            visibility=self.sections.make_visibility_status(),
            access=self._make_section_access(),
            settings=self._make_section_settings(),
            meta_info=self._make_section_meta_info(),
            site_specific_info=self._make_site_specific_info(),
        )

    def _make_section_access(self) -> graph.sections.SectionAccess:
        return graph.sections.SectionAccess(
            read_access_kind=self.sections.make_read_access_kind(),
        )

    def _make_section_settings(self) -> graph.sections.SectionSettings:
        return graph.sections.SectionSettings(
            open_in_new_tab=self.faker.random_element(elements=OrderedDict([(True, 0.01), (False, 0.99)])),
            allow_community_posts=self.faker.random_element(elements=OrderedDict([(True, 0.05), (False, 0.95)])),
            hide_from_entry_editor=self.faker.random_element(elements=OrderedDict([(True, 0.10), (False, 0.90)])),
            lock_posts_after_publishing=self.faker.random_element(elements=OrderedDict([(True, 0.01), (False, 0.99)])),
        )

    def _make_section_meta_info(self) -> graph.sections.SectionMetaInfo:
        return graph.sections.SectionMetaInfo(
            image=self.faker.random_element(elements=(None, self._make_image())),
            link_out=self.faker.uri(),
            meta_tags=tuple(self.faker.stream_random_items(self.faker.word, max_size=5)),
            meta_title=self.faker.sentence(),
            about_html=self._make_about_html(),
        )

    def _make_image(self) -> graph.others.Image:
        return graph.others.Image(id=self.faker.random_int(max=999999))

    def make_user_profile(self, profile_id: Optional[int] = None) -> graph.users.UserProfile:
        user_profile = self._make_user_profile_without_details(profile_id)
        user_profile = replace(user_profile, details=self._make_user_profile_details())
        user_profile = replace(user_profile, user=replace(user_profile.user, details=self._make_user_details()))
        return user_profile

    def _make_user_profile_without_details(self, profile_id: Optional[int] = None) -> graph.users.UserProfile:
        return graph.users.UserProfile(
            id=profile_id or self.faker.random_int(max=99999),
            user=graph.users.User(
                id=self.faker.random_int(max=99999),
                details=None,
            ),
            slug=self.faker.slug(),
            title=self.faker.name(),
            about_html=self._make_about_html(),
            description=self.faker.text(),
            details=None,
        )

    def _make_about_html(self) -> str:
        return '\n'.join(map('<p>{}</p>'.format, self.faker.paragraphs()))

    def _make_user_details(self) -> graph.users.UserDetails:
        return graph.users.UserDetails(
            status=self.make_user_status(),
            emails=frozenset(self.faker.stream_random_items(self.faker.email, max_size=5, min_size=1)),
            groups=frozenset(self.faker.stream_random_items(self._make_user_group, max_size=5)),
            communities=frozenset(self.faker.stream_random_items(self.make_community, max_size=5)),
            access_roles=frozenset(self.faker.stream_random_items(self._make_access_role, max_size=5)),
            last_login_ts=self.faker.random_element(elements=OrderedDict([
                (None, 0.01),
                (self.now - Hours(self.faker.random_int(min=0, max=48)), 0.99)
            ]))
        )

    def _make_user_group(self) -> graph.users.UserGroup:
        return graph.users.UserGroup(slug=self.faker.slug())

    def _make_access_role(self) -> graph.users.AccessRole:
        return graph.users.AccessRole(id=self.faker.random_int(max=9999))

    def _make_user_profile_details(self) -> graph.users.UserProfileDetails:
        return graph.users.UserProfileDetails(
            status=self.make_user_profile_status(),
            site_specific_info=self._make_site_specific_info(),
            lifetime_posts_count=self.faker.random_int(max=999),
        )

    def make_community(self) -> graph.others.Community:
        community = self._make_community_without_details()
        community = replace(community, details=self._make_community_details())
        return community

    def _make_community_without_details(self) -> graph.others.Community:
        return graph.others.Community(
            id=self.faker.random_int(max=999999),
            slug=self.faker.slug(),
            title=self.faker.sentence(nb_words=2),
            about_html=self._make_about_html(),
            description=self.faker.text(),
            details=None,
        )

    def _make_community_details(self) -> graph.others.CommunityDetails:
        return graph.others.CommunityDetails(
            site_specific_info=self._make_site_specific_info(),
            lifetime_posts_count=self.faker.random_int(max=99999),
        )

    def _make_layout_without_details(self) -> graph.others.Layout:
        return graph.others.Layout(
            slug=self.faker.slug(),
        )

    def _make_site_specific_path(self) -> str:
        return '.'.join(self.faker.words())

    def _make_site_specific_info(self) -> Mapping:
        return read_only(self.faker.pydict(5, str, int))

    def make_user_status(self) -> users.consts.USER.STATUS:
        return self.users.make_status()

    def make_user_profile_status(self) -> users.statuses.Status:
        return self.users.make_profile_status()
