from typing import Iterator

from faker import Faker
from faker.providers import lorem
from faker.providers import python
from faker.providers import BaseProvider

from rmshared import faker_ext

from rmshared.content.taxonomy.sections import access
from rmshared.content.taxonomy.sections import consts

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

    def make_visibility_status(self) -> consts.VISIBILITY.STATUS:
        return self.faker.random_element(elements=frozenset(self._stream_visibility_statuses()))

    @staticmethod
    def _stream_visibility_statuses() -> Iterator[consts.VISIBILITY.STATUS]:
        return iter(consts.VISIBILITY.STATUS.ALL)

    def make_read_access_kind(self) -> access.Kind:
        return self.faker.random_element(elements=frozenset(self._stream_read_access_kinds()))

    @staticmethod
    def _stream_read_access_kinds() -> Iterator[access.Kind]:
        yield access.Public()
        yield access.Restricted(is_inherited=True)
        yield access.Restricted(is_inherited=False)
