from typing import Iterable
from typing import Iterator
from typing import Optional
from typing import Type

from faker import Faker
from faker.providers import lorem
from faker.providers import python
from faker.providers import BaseProvider

from rmshared import faker_ext

from rmshared.content.taxonomy import core
from rmshared.content.taxonomy import graph
from rmshared.content.taxonomy import posts
from rmshared.content.taxonomy import users
from rmshared.content.taxonomy import sections
from rmshared.content.taxonomy import variables
from rmshared.content.taxonomy.abc import Guid

FakerWithProviders = Faker | BaseProvider | python.Provider | lorem.Provider | faker_ext.Provider


class Fakes:
    NOW = 1440000000
    SEED = 1231

    def __init__(self, now=NOW, seed=SEED):
        self.now = now
        self.faker: FakerWithProviders = Faker()
        self.faker.add_provider(faker_ext.Provider)
        self.faker.seed_instance(seed)
        self.core = core.Fakes(seed)
        self.graph = graph.Fakes(now, seed)
        self.variables = variables.Fakes(seed)

    def make_guid(self) -> Guid:
        return self.faker.random_element(elements=frozenset(self._stream_guids()))

    def _stream_guids(self) -> Iterator[Guid]:
        yield self.make_post_guid()
        yield self.make_section_guid()
        yield self.make_user_profile_guid()

    def make_post_guid(self) -> posts.guids.Post:
        return posts.guids.Post(id=self.faker.random_int(min=99999, max=99999999))

    def make_section_guid(self) -> sections.guids.Section:
        return sections.guids.Section(id=self.faker.random_int(min=9999, max=9999999))

    def make_user_profile_guid(self) -> users.guids.UserProfile:
        return users.guids.UserProfile(id=self.faker.random_int(min=9999, max=9999999))

    def make_guid_type(self) -> Type[Guid]:
        return self.faker.random_element(elements=frozenset(self._stream_guid_types()))

    def make_guid_type_other_than(self, guid_type: Type[Guid]) -> Type[Guid]:
        return self.faker.random_element(elements=frozenset(self._stream_guid_types()) - frozenset({guid_type}))

    @staticmethod
    def _stream_guid_types() -> Iterator[Type[Guid]]:
        yield posts.guids.Post
        yield sections.guids.Section
        yield users.guids.UserProfile

    def make_post(self, post_id: Optional[int] = None) -> graph.posts.Post:
        return self.graph.make_post(post_id)

    def make_section(self, section_id: Optional[int] = None) -> graph.sections.Section:
        return self.graph.make_section(section_id)

    def make_user_profile(self, profile_id: Optional[int] = None) -> graph.users.UserProfile:
        return self.graph.make_user_profile(profile_id)

    def sample_core_filters(self, max_size: Optional[int] = None, min_size: Optional[int] = None) -> Iterable[core.filters.Filter]:
        return self.core.sample_filters(max_size, min_size)

    def stream_core_filters(self) -> Iterator[core.filters.Filter]:
        return self.core.stream_filters()

    def sample_core_events(self, max_size: Optional[int] = None, min_size: Optional[int] = None) -> Iterable[core.events.Event]:
        return self.core.sample_events(max_size, min_size)

    def make_core_field(self) -> core.fields.Field:
        return self.core.make_field()

    def sample_variable_filters(self) -> Iterator[variables.Operator[core.filters.Filter]]:
        return self.variables.sample_filters()

    def sample_variable_argument_types(self, size: Optional[int] = None) -> Iterable[Type[variables.Argument]]:
        return self.variables.sample_argument_types(size)
