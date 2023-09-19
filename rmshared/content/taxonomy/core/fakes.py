from typing import Callable
from typing import Iterator
from typing import Optional
from typing import TypeVar

from faker import Faker
from faker.providers import BaseProvider
from faker.providers import lorem
from faker.providers import python

from rmshared import faker_ext

from rmshared.content.taxonomy.core import filters
from rmshared.content.taxonomy.core import labels
from rmshared.content.taxonomy.core import ranges
from rmshared.content.taxonomy.core import fields
from rmshared.content.taxonomy.core import events

FakerWithProviders = Faker | BaseProvider | lorem.Provider | python.Provider | faker_ext.Provider
Label = TypeVar('Label')
Range = TypeVar('Range')


class Fakes:
    NOW = 1440000000
    SEED = 1231

    def __init__(self, now=NOW, seed=SEED):
        self.now = now
        self.faker: FakerWithProviders = Faker()
        self.faker.add_provider(faker_ext.Provider)
        self.faker.seed_instance(seed)

    def sample_filters(self, max_size: Optional[int] = None, min_size: Optional[int] = None) -> Iterator[filters.Filter]:
        min_size = 3 if min_size is None else min_size
        max_size = 5 if max_size is None else max_size
        return self.faker.stream_random_items(factory_func=self.make_filter, max_size=max_size, min_size=min_size)

    def make_filter(self) -> filters.Filter:
        return self.faker.random_element(elements=frozenset(self.stream_filters()))

    def stream_filters(self) -> Iterator[filters.Filter]:
        return self.stream_generic_filters(self._sample_labels, self._sample_ranges)

    @staticmethod
    def stream_generic_filters(stream_labels: Callable[[], Iterator[Label]], stream_ranges: Callable[[], Iterator[Range]]) -> Iterator[filters.Filter]:
        yield filters.AnyLabel(labels=tuple(stream_labels()))
        yield filters.NoLabels(labels=tuple(stream_labels()))
        yield filters.AnyRange(ranges=tuple(stream_ranges()))
        yield filters.NoRanges(ranges=tuple(stream_ranges()))

    def _sample_labels(self) -> Iterator[labels.Label]:
        return self.faker.stream_random_items(factory_func=self.make_label, min_size=1, max_size=3)

    def make_label(self) -> labels.Label:
        return self.faker.random_element(elements=frozenset(self._stream_labels()))

    def _stream_labels(self) -> Iterator[labels.Label]:
        yield labels.Value(field=self.make_field(), value=self.make_scalar())
        yield labels.Badge(field=self.make_field())
        yield labels.Empty(field=self.make_field())

    def _sample_ranges(self) -> Iterator[ranges.Range]:
        return self.faker.stream_random_items(factory_func=self.make_range, min_size=1, max_size=3)

    def make_range(self) -> ranges.Range:
        return self.faker.random_element(elements=frozenset(self._stream_ranges()))

    def _stream_ranges(self) -> Iterator[ranges.Range]:
        yield ranges.Between(field=self.make_field(), min_value=self.make_scalar(), max_value=self.make_scalar())
        yield ranges.LessThan(field=self.make_field(), value=self.make_scalar())
        yield ranges.MoreThan(field=self.make_field(), value=self.make_scalar())

    def make_field(self) -> fields.Field:
        return self.faker.random_element(elements=frozenset(self._stream_fields()))

    def _stream_fields(self) -> Iterator[fields.Field]:
        yield fields.System(name=self.faker.word())
        yield fields.Custom(name=self.faker.word(), path='.'.join(self.faker.words()))

    def sample_events(self, max_size: Optional[int] = None, min_size: Optional[int] = None) -> Iterator[events.Event]:
        min_size = 1 if min_size is None else min_size
        max_size = 5 if max_size is None else max_size
        return self.faker.stream_random_items(factory_func=self.make_event, max_size=max_size, min_size=min_size)

    def make_event(self) -> events.Event:
        return events.Event(name='-'.join(self.faker.words()))

    def make_scalar(self):
        return self.faker.random_element(elements=frozenset(self._stream_scalars()))

    def _stream_scalars(self) -> Iterator[str | int | float]:
        yield self.faker.pystr()
        yield self.faker.pyint()
        yield self.faker.pyfloat()
