from dataclasses import replace
from typing import Callable
from typing import Iterable
from typing import Iterator
from typing import Optional
from typing import Type
from typing import TypeVar

from faker import Faker
from faker.providers import BaseProvider
from faker.providers import lorem
from faker.providers import python

from rmshared import faker_ext
from rmshared.tools import as_is
from rmshared.tools import dict_from_list
from rmshared.tools import ensure_map_is_complete
from rmshared.typings import read_only

from rmshared.content.taxonomy.core import filters
from rmshared.content.taxonomy.core import labels
from rmshared.content.taxonomy.core import ranges
from rmshared.content.taxonomy.core import fields
from rmshared.content.taxonomy.core import variables

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

    def make_filter(self) -> filters.Filter:
        return self.faker.random_element(elements=frozenset(self._stream_filters()))

    def _stream_filters(self) -> Iterator[filters.Filter]:
        yield filters.AnyLabel(labels=tuple(self._stream_random_labels()))
        yield filters.NoLabels(labels=tuple(self._stream_random_labels()))
        yield filters.AnyRange(ranges=tuple(self._stream_random_ranges()))
        yield filters.NoRanges(ranges=tuple(self._stream_random_ranges()))

    def _stream_random_labels(self) -> Iterator[labels.Label]:
        return self.faker.stream_random_items(self.make_label, min_size=1, max_size=3)

    def make_label(self) -> labels.Label:
        return self.faker.random_element(elements=frozenset(self._stream_labels()))

    def _stream_labels(self) -> Iterator[labels.Label]:
        yield labels.Value(field=self.make_field(), value=self.make_scalar())
        yield labels.Badge(field=self.make_field())
        yield labels.Empty(field=self.make_field())

    def _stream_random_ranges(self) -> Iterator[ranges.Range]:
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

    def make_scalar(self):
        return self.faker.random_element(elements=frozenset(self._stream_scalars()))

    def _stream_scalars(self) -> Iterator[str | int | float]:
        yield self.faker.pystr()
        yield self.faker.pyint()
        yield self.faker.pyfloat()

    def stream_variable_filters(self) -> Iterator[variables.Operator[filters.Filter]]:
        return self.variables.stream_filters()

    def sample_variable_argument_types(self, size: Optional[int] = None) -> Iterable[Type[variables.Argument]]:
        return self.variables.sample_argument_types(size)

    class Variables:
        Case = TypeVar('Case')

        def __init__(self, fakes: 'Fakes'):
            self.fakes = fakes
            self.faker = fakes.faker
            self.label_to_replace_values_func_map = ensure_map_is_complete(labels.Label, {
                labels.Value: self._replace_value_label_value_with_variable_value,
                labels.Badge: as_is,
                labels.Empty: as_is,
            })
            self.range_to_replace_values_func_map = ensure_map_is_complete(ranges.Range, {
                ranges.Between: self._replace_between_range_values_with_variable_values,
                ranges.LessThan: self._replace_less_than_range_value_with_variable_value,
                ranges.MoreThan: self._replace_more_than_range_value_with_variable_value,
            })

        def stream_filters(self) -> Iterator[variables.Operator[filters.Filter]]:
            yield self._make_switch_operator(make_case=self._make_filter)
            yield self._make_return_operator(make_case=self._make_filter)

        def _make_filter(self) -> filters.Filter:
            return self.fakes.make_filter()

        def stream_labels(self) -> Iterator[variables.Operator[labels.Label]]:
            yield self._make_switch_operator(make_case=self._make_label)
            yield self._make_return_operator(make_case=self._make_label)

        def _make_label(self) -> labels.Label:
            label = self.fakes.make_label()
            label = self._replace_label_values_with_variable_values(label)
            return label

        def _replace_label_values_with_variable_values(self, label: labels.Label) -> labels.Label:
            return self.label_to_replace_values_func_map[type(label)](label)

        def _replace_value_label_value_with_variable_value(self, label: labels.Value) -> labels.Value:
            return replace(label, value=self._make_variable_value())

        def stream_ranges(self) -> Iterator[variables.Operator[ranges.Range]]:
            yield self._make_switch_operator(make_case=self._make_range)
            yield self._make_return_operator(make_case=self._make_range)

        def _make_range(self) -> ranges.Range:
            range_ = self.fakes.make_range()
            range_ = self._replace_range_values_with_variable_values(range_)
            return range_

        def _replace_range_values_with_variable_values(self, range_: ranges.Range) -> ranges.Range:
            return self.range_to_replace_values_func_map[type(range_)](range_)

        def _replace_between_range_values_with_variable_values(self, range_: ranges.Between) -> ranges.Between:
            return replace(range_, min_value=self._make_variable_value(), max_value=self._make_variable_value())

        def _replace_less_than_range_value_with_variable_value(self, range_: ranges.LessThan) -> ranges.LessThan:
            return replace(range_, value=self._make_variable_value())

        def _replace_more_than_range_value_with_variable_value(self, range_: ranges.MoreThan) -> ranges.MoreThan:
            return replace(range_, value=self._make_variable_value())

        def _make_switch_operator(self, make_case: Callable[[], Case]) -> variables.operators.Switch[Case]:
            return variables.operators.Switch(
                ref=self._make_reference(),
                cases=read_only(dict_from_list(self._stream_argument_types(), value_func=lambda _: self._make_return_operator(make_case))),
            )

        def _make_return_operator(self, make_case: Callable[[], Case]) -> variables.operators.Return[Case]:
            return variables.operators.Return(
                cases=tuple(self.faker.stream_random_items(make_case, min_size=1, max_size=3)),
            )

        def _make_variable_value(self) -> variables.values.Value:
            return self.faker.random_element(elements={
                self.make_variable(),
                self.make_constant(),
            })

        def make_variable(self) -> variables.values.Variable:
            return variables.values.Variable(ref=self._make_reference(), index=self.faker.random_int(min=1, max=5))

        def make_constant(self) -> variables.values.Constant:
            return variables.values.Constant(value=self.fakes.make_scalar())

        def _make_reference(self):
            return variables.Reference(alias=self.faker.word())

        def sample_argument_types(self, size: Optional[int] = None) -> Iterable[Type[variables.Argument]]:
            return self.faker.random_sample(elements=tuple(self._stream_argument_types()), length=size)

        @staticmethod
        def _stream_argument_types() -> Iterator[Type[variables.Argument]]:
            yield variables.arguments.Value
            yield variables.arguments.Empty
            yield variables.arguments.Any
