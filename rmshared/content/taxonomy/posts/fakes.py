from typing import Collection
from typing import Iterator
from typing import Type

from faker import Faker
from faker.providers import lorem
from faker.providers import python
from faker.providers import BaseProvider

from rmshared import faker_ext

from rmshared.content.taxonomy.posts import consts
from rmshared.content.taxonomy.posts import statuses

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

    def make_type(self) -> consts.POST.TYPE:
        return self.faker.random_element(elements=frozenset(self._stream_types()))

    @staticmethod
    def _stream_types() -> Iterator[consts.POST.TYPE]:
        return iter(consts.POST.TYPE.ALL)

    def make_status(self) -> statuses.Status:
        return self.faker.random_element(elements=frozenset(self._stream_statuses()))

    def make_status_other_than(self, status_types: Collection[Type[statuses.Status]]) -> statuses.Status:
        return self.faker.random_element(elements=frozenset(self._stream_statuses_other_than(status_types)))

    def _stream_statuses_other_than(self, status_types: Collection[Type[statuses.Status]]) -> Iterator[statuses.Status]:
        def unless_excluded(status: statuses.Status) -> bool:
            return type(status) not in status_types

        return filter(unless_excluded, self._stream_statuses())

    def _stream_statuses(self) -> Iterator[statuses.Status]:
        yield statuses.Draft(stage=self.make_draft_stage())
        yield statuses.Published(scope=self.make_published_scope())
        yield statuses.Removed()

    def make_draft_stage(self) -> statuses.drafts.stages.Stage:
        return self.faker.random_element(elements=frozenset(self._stream_draft_stages()))

    @staticmethod
    def _stream_draft_stages() -> Iterator[statuses.drafts.stages.Stage]:
        yield statuses.drafts.stages.Created(is_imported=True)
        yield statuses.drafts.stages.Created(is_imported=False)
        yield statuses.drafts.stages.InProgress(is_rejected=True)
        yield statuses.drafts.stages.InProgress(is_rejected=False)
        yield statuses.drafts.stages.InReview()
        yield statuses.drafts.stages.Ready()

    def make_published_scope(self) -> statuses.published.scopes.Scope:
        return self.faker.random_element(elements=frozenset(self._stream_published_scopes()))

    @staticmethod
    def _stream_published_scopes() -> Iterator[statuses.published.scopes.Scope]:
        yield statuses.published.scopes.Site(is_promoted=True)
        yield statuses.published.scopes.Site(is_promoted=False)
        yield statuses.published.scopes.Community(is_demoted=True)
        yield statuses.published.scopes.Community(is_demoted=False)
