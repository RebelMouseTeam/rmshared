from collections import OrderedDict
from typing import Collection
from typing import Iterator
from typing import Tuple
from typing import Type

from faker import Faker
from faker.providers import lorem
from faker.providers import python
from faker.providers import BaseProvider

from rmshared import faker_ext

from rmshared.content.taxonomy.users import consts
from rmshared.content.taxonomy.users import statuses

FakerWithProviders = Faker | BaseProvider | python.Provider | lorem.Provider | faker_ext.Provider


class Fakes:
    NOW = 1440000000
    SEED = 1231

    def __init__(self, now=NOW, seed=SEED):
        self.now = now
        self.faker: FakerWithProviders = Faker()
        self.faker.add_provider(faker_ext.Provider)
        self.faker.seed_instance(seed)

    def make_id(self) -> int:
        return self.faker.random_int()

    def make_status(self) -> consts.USER.STATUS:
        return self.faker.random_element(elements=frozenset(self._stream_statuses()))

    @staticmethod
    def _stream_statuses() -> Iterator[consts.USER.STATUS]:
        return iter(consts.USER.STATUS.ALL)

    def make_profile_status(self) -> statuses.Status:
        return self.make_profile_status_other_than(status_types=frozenset())

    def make_profile_status_other_than(self, status_types: Collection[Type[statuses.Status]]) -> statuses.Status:
        return self.faker.random_element(elements=OrderedDict(self._stream_profile_statuses_other_than(status_types)))

    def _stream_profile_statuses_other_than(self, status_types: Collection[Type[statuses.Status]]) -> Iterator[Tuple[statuses.Status, float]]:
        def unless_excluded(status_with_probability: Tuple[statuses.Status, float]) -> bool:
            return type(status_with_probability[0]) not in status_types

        return filter(unless_excluded, self._stream_profile_statuses())

    @staticmethod
    def _stream_profile_statuses() -> Iterator[Tuple[statuses.Status, float]]:
        yield statuses.Pending(), 0.10
        yield statuses.Active(), 0.70,
        yield statuses.Inactive(is_banned=True), 0.10
        yield statuses.Inactive(is_banned=False), 0.10
