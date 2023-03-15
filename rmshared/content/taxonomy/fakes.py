from collections import OrderedDict
from dataclasses import replace
from itertools import filterfalse
from typing import AbstractSet
from typing import FrozenSet
from typing import Iterable
from typing import Iterator
from typing import Optional
from typing import Tuple
from typing import Type
from typing import TypeVar

from faker import Faker
from faker.providers import lorem
from faker.providers import python
from faker.providers import BaseProvider

from rmshared import faker_ext
from rmshared.tools import ensure_map_is_complete
from rmshared.typings import read_only

from rmshared.content.taxonomy import core0
from rmshared.content.taxonomy import groupings
from rmshared.content.taxonomy import posts
from rmshared.content.taxonomy import users
from rmshared.content.taxonomy import filters
from rmshared.content.taxonomy import orders
from rmshared.content.taxonomy.abc import Guid
from rmshared.content.taxonomy.abc import Text
from rmshared.content.taxonomy.abc import Label
from rmshared.content.taxonomy.abc import Field
from rmshared.content.taxonomy.abc import Value
from rmshared.content.taxonomy.abc import Aspects
from rmshared.content.taxonomy.abc import Entity
from rmshared.content.taxonomy.abc import Filter
from rmshared.content.taxonomy.abc import Order
from rmshared.content.taxonomy.abc import Chunk
from rmshared.content.taxonomy.abc import Grouping

T = TypeVar('T')
FakerWithProviders = Faker | BaseProvider | python.Provider | lorem.Provider | faker_ext.Provider


class Fakes:
    NOW = 1440000000
    SEED = 1231

    def __init__(self, now=NOW, seed=SEED):
        self.now = now
        self.faker: FakerWithProviders = Faker()
        self.faker.add_provider(faker_ext.Provider)
        self.faker.seed_instance(seed)
        self.core = core0.Fakes(seed)
        self.guid_to_entity_factory_map = ensure_map_is_complete(Guid, {
            None: self._pick_entity,
            posts.guids.Post: self.make_post,
            users.guids.UserProfile: self.make_user_profile,
        })
        self.guid_to_aspects_factory_map = ensure_map_is_complete(Guid, {
            None: self._pick_aspects,
            posts.guids.Post: self.make_post_aspects,
            users.guids.UserProfile: self.make_user_profile_aspects,
        })

    def make_entity_without_aspects(self) -> Entity:
        entity = self.make_entity()
        entity = replace(entity, aspects=None)
        return entity

    def make_entity(self, guid_type: Optional[Type[Guid]] = None) -> Entity:
        return self.guid_to_entity_factory_map[guid_type]()

    def _pick_entity(self) -> Entity:
        return self.faker.random_element(elements={
            self.make_post(),
            self.make_user_profile(),
        })

    def make_post(self) -> Entity:
        return Entity(
            guid=self.make_post_guid(),
            aspects=self.make_post_aspects(),
        )

    def make_user_profile(self) -> Entity:
        return Entity(
            guid=self.make_user_profile_guid(),
            aspects=self.make_user_profile_aspects(),
        )

    def make_guid(self):
        return self.faker.random_element(elements={
            self.make_post_guid(),
            self.make_user_profile_guid(),
        })

    def make_post_guid(self) -> posts.guids.Post:
        return posts.guids.Post(id=self.faker.random_int(min=99999, max=99999999))

    def make_user_profile_guid(self) -> users.guids.UserProfile:
        return users.guids.UserProfile(id=self.faker.random_int(min=9999, max=9999999))

    def make_guid_type(self) -> Type[Guid]:
        return self.faker.random_element(elements=self._make_guid_types())

    def make_guid_type_other_than(self, guid_type: Type[Guid]) -> Type[Guid]:
        return self.faker.random_element(elements=self._make_guid_types() - {guid_type})

    @staticmethod
    def _make_guid_types() -> AbstractSet[Type[Guid]]:
        return {
            posts.guids.Post,
            users.guids.UserProfile,
        }

    def make_aspects(self, guid_type: Optional[Type[Guid]] = None) -> Aspects:
        return self.guid_to_aspects_factory_map[guid_type]()

    def _pick_aspects(self) -> Aspects:
        return self.faker.random_element(elements={
            self.make_post_aspects(),
            self.make_user_profile_aspects(),
        })

    def make_post_aspects(self) -> Aspects:  # TODO: add other aspects
        return Aspects(
            texts=frozenset(),
            labels=frozenset({
                self._make_post_primary_section_label(),
                self._make_post_regular_section_label(),
            }),
            values=frozenset({
                self._make_post_published_at_value(),
            }),
            extras=read_only(self.faker.pydict(nb_elements=5, value_types=(str, int, float))),
        )

    def make_user_profile_aspects(self) -> Aspects:
        return Aspects(
            texts=frozenset(),
            labels=frozenset(),
            values=frozenset(),
            extras=read_only(self.faker.pydict(nb_elements=5, value_types=(str, int, float))),
        )

    def make_filters(self) -> FrozenSet[Filter]:
        return frozenset(self.faker.stream_random_items(self._make_filter, max_size=5))

    def _make_filter(self):  # TODO: add other filters
        return self.faker.random_element(elements={
            filters.Phrase(phrase=self.faker.sentence(), syntax=None, weights=None),
        })

    def _make_post_primary_section_label(self) -> posts.labels.PrimarySection:
        return posts.labels.PrimarySection(id=self.faker.random_int(max=99999))

    def _make_post_regular_section_label(self) -> posts.labels.RegularSection:
        return posts.labels.RegularSection(id=self.faker.random_int(max=99999))

    def _make_post_published_at_value(self) -> Value:
        return Value(field=posts.fields.PublishedAt(), value=self.faker.unix_time())

    def make_chunk(self) -> Chunk:
        return Chunk(
            order=self.faker.random_element(elements=frozenset(self._stream_orders())),
            limit=self.faker.random_int(max=20),
            offset=self.faker.random_int(max=5),
            cursor=self.faker.random_element(elements=frozenset([None, self._make_cursor()])),
        )

    def _stream_orders(self) -> Iterator[Order]:
        yield orders.Value(field=self.make_field(), reverse=self.faker.pybool())
        yield orders.Relevance(decay=self.faker.random_element(elements={None, self._make_relevance_order_decay()}))

    def _make_relevance_order_decay(self) -> orders.Decay:
        return orders.Decay(field=self.make_field(), speed=self.faker.random_int(min=0, max=10))

    def _make_cursor(self):
        return ':'.join(self.faker.words())

    def make_grouping(self) -> Grouping:
        return self.faker.random_element(elements=[
            self._make_labels_grouping(),
        ])

    def _make_labels_grouping(self) -> groupings.Labels:
        return groupings.Labels(
            labels=frozenset(self.faker.stream_random_items(self.make_label, max_size=20))
        )

    def make_text(self) -> Text:  # TODO: add more texts
        return self.faker.random_element(elements={
            posts.texts.Titles(),
        })

    def make_label(self) -> Label:  # TODO: add more labels
        return self.faker.random_element(elements={
            posts.labels.Status(status=self.make_post_status()),
        })

    def make_field(self) -> Field:  # TODO: add more fields
        return self.faker.random_element(elements={
            posts.fields.PublishedAt()
        })

    def make_post_status_other_than(self, status_type: Type[posts.statuses.Status]) -> posts.statuses.Status:
        return self.faker.random_element(elements=tuple(self._stream_post_statuses_other_than(status_type)))

    def _stream_post_statuses_other_than(self, status_type: Type[posts.statuses.Status]) -> Iterator[posts.statuses.Status]:
        return filterfalse(lambda status: isinstance(status, status_type), self._stream_post_statuses())

    def make_post_status(self) -> posts.statuses.Status:
        return self.faker.random_element(elements=tuple(self._stream_post_statuses()))

    def _stream_post_statuses(self) -> Iterator[posts.statuses.Status]:
        yield posts.statuses.Draft(stage=self.make_draft_post_stage())
        yield posts.statuses.Published(scope=self.make_published_post_scope())
        yield posts.statuses.Removed()

    def make_draft_post_stage(self) -> posts.drafts.stages.Stage:
        return self.faker.random_element(elements=(
            posts.drafts.stages.Created(is_imported=True),
            posts.drafts.stages.Created(is_imported=False),
            posts.drafts.stages.InProgress(is_rejected=True),
            posts.drafts.stages.InProgress(is_rejected=False),
            posts.drafts.stages.InReview(),
            posts.drafts.stages.Ready(),
        ))

    def make_published_post_scope(self) -> posts.published.scopes.Scope:
        return self.faker.random_element(elements=(
            posts.published.scopes.Site(is_promoted=True),
            posts.published.scopes.Site(is_promoted=False),
            posts.published.scopes.Community(is_demoted=True),
            posts.published.scopes.Community(is_demoted=False),
        ))

    def make_user_status(self):
        return self.faker.random_element(elements=users.consts.USER.STATUS.ALL)

    def make_user_profile_status(self):
        return self.faker.random_element(
            elements=OrderedDict(self._stream_user_profile_statuses_with_probabilities())
        )

    @staticmethod
    def _stream_user_profile_statuses_with_probabilities() -> Iterator[Tuple[users.statuses.Status, float]]:
        yield users.statuses.Pending(), 0.10
        yield users.statuses.Active(), 0.70,
        yield users.statuses.Inactive(is_banned=True), 0.10
        yield users.statuses.Inactive(is_banned=False), 0.10

    def stream_core0_variable_filters(self) -> Iterator[core0.Filter]:
        return self.core.stream_variable_filters()

    def sample_core0_variable_argument_types(self, size: Optional[int] = None) -> Iterable[Type[core0.variables.Argument]]:
        return self.core.sample_variable_argument_types(size)
