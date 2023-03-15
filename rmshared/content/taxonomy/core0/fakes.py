from itertools import chain
from typing import Any
from typing import Iterable
from typing import Iterator
from typing import Optional
from typing import Type

from faker import Faker
from faker.providers import BaseProvider
from faker.providers import lorem
from faker.providers import python

from rmshared import faker_ext
from rmshared.typings import read_only
from rmshared.tools import dict_from_list

from rmshared.content.taxonomy.core0 import filters
from rmshared.content.taxonomy.core0 import labels
from rmshared.content.taxonomy.core0 import ranges
from rmshared.content.taxonomy.core0 import fields
from rmshared.content.taxonomy.core0 import variables
from rmshared.content.taxonomy.core0.abc import Filter
from rmshared.content.taxonomy.core0.abc import Label
from rmshared.content.taxonomy.core0.abc import Range
from rmshared.content.taxonomy.core0.abc import Field

FakerWithProviders = Faker | BaseProvider | lorem.Provider | python.Provider | faker_ext.Provider


class Fakes:
    NOW = 1440000000
    SEED = 1231

    def __init__(self, now=NOW, seed=SEED):
        self.now = now
        self.faker: FakerWithProviders = Faker()
        self.faker.add_provider(faker_ext.Provider)
        self.faker.seed_instance(seed)
        self.variables = self.Variables(self)

    def make_filter(self) -> Filter:
        return self.faker.random_element(elements=frozenset(self._stream_filters()))

    def _stream_filters(self) -> Iterator[Filter]:
        yield filters.AnyLabel(labels=tuple(self._stream_random_labels()))
        yield filters.NoLabels(labels=tuple(self._stream_random_labels()))
        yield filters.AnyRange(ranges=tuple(self._stream_random_ranges()))
        yield filters.NoRanges(ranges=tuple(self._stream_random_ranges()))

    def _stream_random_labels(self) -> Iterator[Label]:
        return self.faker.stream_random_items(self.make_label, min_size=1, max_size=3)

    def make_label(self) -> Label:
        return self.faker.random_element(elements=frozenset(self._stream_labels()))

    def _stream_labels(self) -> Iterator[Label]:
        yield labels.Value(field=self.make_field(), value=self.make_scalar())
        yield labels.Badge(field=self.make_field())
        yield labels.Empty(field=self.make_field())

    def _stream_random_ranges(self) -> Iterator[Range]:
        return self.faker.stream_random_items(factory_func=self.make_range, min_size=1, max_size=3)

    def make_range(self) -> Range:
        return self.faker.random_element(elements=frozenset(self._stream_ranges()))

    def _stream_ranges(self) -> Iterator[Range]:
        yield ranges.Between(field=self.make_field(), min_value=self.make_scalar(), max_value=self.make_scalar())
        yield ranges.LessThan(field=self.make_field(), value=self.make_scalar())
        yield ranges.MoreThan(field=self.make_field(), value=self.make_scalar())

    def make_field(self) -> Field:
        return self.faker.random_element(elements=frozenset(self._stream_fields()))

    def _stream_fields(self) -> Iterator[Field]:
        yield fields.System(name=self.faker.word())
        yield fields.Custom(name=self.faker.word(), path='.'.join(self.faker.words()))

    def make_scalar(self):
        return self.faker.random_element(elements=frozenset(self._stream_scalars()))

    def _stream_scalars(self) -> Iterator[str | int | float]:
        yield self.faker.pystr()
        yield self.faker.pyint()
        yield self.faker.pyfloat()

    def stream_variable_filters(self) -> Iterator[Filter]:
        return self.variables.stream_filters()

    def sample_variable_argument_types(self, size: Optional[int] = None) -> Iterable[Type[variables.Argument]]:
        return self.variables.sample_argument_types(size)

    class Variables:
        def __init__(self, fakes: 'Fakes'):
            self.fakes = fakes
            self.faker = fakes.faker

        def stream_filters(self) -> Iterator[Filter]:
            yield filters.AnyLabel(labels=tuple(self._stream_random_labels()))
            yield filters.NoLabels(labels=tuple(self._stream_random_labels()))
            yield filters.AnyRange(ranges=tuple(self._stream_random_ranges()))
            yield filters.NoRanges(ranges=tuple(self._stream_random_ranges()))
            yield variables.filters.Switch(ref=self._make_reference(), cases=self._make_cases(make_case_item=self.fakes.make_filter))

        def _stream_random_labels(self) -> Iterator[Label]:
            return self.faker.stream_random_items(self.make_label, min_size=1, max_size=3)

        def make_label(self) -> Label:
            return self.faker.random_element(elements=frozenset(chain(self._stream_labels(), self.fakes._stream_labels())))

        def _stream_labels(self) -> Iterator[Label]:
            yield variables.labels.Value(field=self.fakes.make_field(), value=self.make_variable())
            yield variables.labels.Switch(ref=self._make_reference(), cases=self._make_cases(make_case_item=self.fakes.make_label))

        def _stream_random_ranges(self) -> Iterator[Range]:
            return self.faker.stream_random_items(factory_func=self.make_range, min_size=1, max_size=3)

        def make_range(self) -> Range:
            return self.faker.random_element(elements=frozenset(chain(self._stream_ranges(), self.fakes._stream_ranges())))

        def _stream_ranges(self) -> Iterator[Range]:
            yield variables.ranges.Between(
                field=self.fakes.make_field(), min_value=self._make_variable_or_constant(), max_value=self._make_variable_or_constant()
            )
            yield variables.ranges.LessThan(field=self.fakes.make_field(), value=self.make_variable())
            yield variables.ranges.MoreThan(field=self.fakes.make_field(), value=self.make_variable())
            yield variables.ranges.Switch(ref=self._make_reference(), cases=self._make_cases(make_case_item=self.fakes.make_range))

        def _make_variable_or_constant(self) -> variables.Variable | variables.Constant:
            return self.faker.random_element(elements={
                self.make_variable(),
                self.make_constant(),
            })

        def make_variable(self) -> variables.Variable:
            return variables.Variable(ref=self._make_reference(), index=self.faker.random_int(min=1, max=5))

        def make_constant(self) -> variables.Constant:
            return variables.Constant(value=self.fakes.make_scalar())

        def _make_reference(self):
            return variables.Reference(alias=self.faker.word())

        def _make_cases(self, make_case_item):
            def make_case(_: Any):
                return tuple(self.faker.stream_random_items(factory_func=make_case_item, min_size=1, max_size=3))

            return variables.Cases(
                cases=read_only(dict_from_list(self._stream_argument_types(), value_func=make_case)),
            )

        def sample_argument_types(self, size: Optional[int] = None) -> Iterable[Type[variables.Argument]]:
            return self.faker.random_sample(elements=tuple(self._stream_argument_types()), length=size)

        @staticmethod
        def _stream_argument_types() -> Iterator[Type[variables.Argument]]:
            yield variables.arguments.Value
            yield variables.arguments.Empty
            yield variables.arguments.Any
