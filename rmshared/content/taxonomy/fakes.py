from typing import FrozenSet
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
from rmshared.content.taxonomy import filters
from rmshared.content.taxonomy.abc import Guid
from rmshared.content.taxonomy.abc import Filter

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

    def make_guid(self) -> Guid:
        return self.faker.random_element(elements=frozenset(self._stream_guids()))

    def _stream_guids(self) -> Iterator[Guid]:
        yield self._make_post_guid()
        yield self._make_user_profile_guid()

    def _make_post_guid(self) -> posts.guids.Post:
        return posts.guids.Post(id=self.faker.random_int(min=99999, max=99999999))

    def _make_user_profile_guid(self) -> users.guids.UserProfile:
        return users.guids.UserProfile(id=self.faker.random_int(min=9999, max=9999999))

    def make_guid_type(self) -> Type[Guid]:
        return self.faker.random_element(elements=frozenset(self._stream_guid_types()))

    def make_guid_type_other_than(self, guid_type: Type[Guid]) -> Type[Guid]:
        return self.faker.random_element(elements=frozenset(self._stream_guid_types()) - frozenset({guid_type}))

    @staticmethod
    def _stream_guid_types() -> Iterator[Type[Guid]]:
        yield posts.guids.Post
        yield users.guids.UserProfile

    def make_filters(self) -> FrozenSet[Filter]:
        return frozenset(self.faker.stream_random_items(self._make_filter, max_size=5))

    def _make_filter(self):  # TODO: add other filters
        return self.faker.random_element(elements={
            filters.Phrase(phrase=self.faker.sentence(), syntax=None, weights=None),
        })

    def make_post(self) -> graph.posts.Post:
        return self.graph.make_post()

    def make_user_profile(self) -> graph.users.UserProfile:
        return self.graph.make_user_profile()

    def stream_core_filters(self) -> Iterator[core.filters.Filter]:
        return self.core.stream_filters()

    def stream_core_variable_filters(self) -> Iterator[core.variables.Operator[core.filters.Filter]]:
        return self.core.stream_variable_filters()

    def sample_core_variable_argument_types(self, size: Optional[int] = None) -> Iterable[Type[core.variables.Argument]]:
        return self.core.sample_variable_argument_types(size)

    def make_core_order(self) -> core.orders.Order:
        return self.core.make_order()

    def make_core_field(self) -> core.fields.Field:
        return self.core.make_field()
