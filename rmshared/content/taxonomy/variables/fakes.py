from __future__ import annotations

from dataclasses import replace
from typing import Callable
from typing import Iterable
from typing import Iterator
from typing import Mapping
from typing import Optional
from typing import Type
from typing import TypeVar

from faker import Faker
from faker.providers import lorem
from faker.providers import python
from faker.providers import BaseProvider

from rmshared import faker_ext

from rmshared.tools import as_is
from rmshared.tools import dict_from_list
from rmshared.tools import ensure_map_is_complete
from rmshared.typings import read_only

from rmshared.content.taxonomy import core
from rmshared.content.taxonomy.variables import arguments
from rmshared.content.taxonomy.variables import operators
from rmshared.content.taxonomy.variables import values
from rmshared.content.taxonomy.variables.abc import Reference

FakerWithProviders = Faker | BaseProvider | lorem.Provider | python.Provider | faker_ext.Provider

Case = TypeVar('Case')
Range = TypeVar('Range', bound=core.ranges.Range)


class Fakes:
    NOW = 1440000000
    SEED = 1231

    def __init__(self, now=NOW, seed=SEED):
        self.now = now
        self.faker: FakerWithProviders = Faker()
        self.faker.add_provider(faker_ext.Provider)
        self.faker.seed_instance(seed)
        self.core = core.Fakes(now, seed)
        self.values = self.Values(self)

    def make_operator(self) -> operators.Operator[object]:
        return self.faker.random_element(elements=frozenset(self._stream_operators()))

    def _stream_operators(self) -> Iterator[operators.Operator[object]]:
        yield self._make_switch_operator(make_case=lambda: object())
        yield self._make_return_operator(make_case=lambda: object(), max_size=1)

    def make_argument_type(self) -> Type[arguments.Argument]:
        return self.faker.random_element(elements=frozenset(self._stream_argument_types()))

    def sample_argument_types(self, size: Optional[int] = None) -> Iterable[Type[arguments.Argument]]:
        return self.faker.random_sample(elements=tuple(self._stream_argument_types()), length=size)

    @staticmethod
    def _stream_argument_types() -> Iterator[Type[arguments.Argument]]:
        yield arguments.Value
        yield arguments.Empty
        yield arguments.Any

    def make_filter_operator(self) -> operators.Operator[core.filters.Filter]:
        return self.faker.random_element(elements=frozenset(self._stream_filter_operators()))

    def _stream_filter_operators(self) -> Iterator[operators.Operator[core.filters.Filter]]:
        yield self._make_switch_operator(make_case=self._make_filter_with_returns)
        yield self._make_return_operator(make_case=self._make_filter_with_switches)

    def sample_filters(self) -> Iterator[operators.Operator[core.filters.Filter]]:
        return self.faker.stream_random_items(factory_func=self.make_filter_operator, min_size=3, max_size=5)

    def make_label_operator(self) -> operators.Operator[core.labels.Label]:
        return self.faker.random_element(elements=frozenset(self._stream_label_operators()))

    def make_range_operator(self) -> operators.Operator[core.ranges.Range]:
        return self.faker.random_element(elements=frozenset(self._stream_range_operators()))

    def _make_filter_with_returns(self) -> core.filters.Filter:
        def sample_label_operators():
            yield self._make_return_operator(make_case=self._make_label)

        def sample_range_operators():
            yield self._make_return_operator(make_case=self._make_range)

        filters_ = self.core.stream_generic_filters(sample_label_operators, sample_range_operators)
        return self.faker.random_element(elements=frozenset(filters_))

    def _make_filter_with_switches(self) -> core.filters.Filter:
        filters_ = self.core.stream_generic_filters(self._sample_label_operators, self._sample_range_operators)
        return self.faker.random_element(elements=frozenset(filters_))

    def _sample_label_operators(self) -> Iterator[operators.Operator[core.labels.Label]]:
        return self.faker.stream_random_items(factory_func=self._make_label_operator, min_size=1, max_size=3)

    def _make_label_operator(self) -> operators.Operator[core.labels.Label]:
        return self.faker.random_element(elements=frozenset(self._stream_label_operators()))

    def _stream_label_operators(self) -> Iterator[operators.Operator[core.labels.Label]]:
        yield self._make_switch_operator(make_case=self._make_label)
        yield self._make_return_operator(make_case=self._make_label)

    def _make_label(self) -> core.labels.Label:
        label = self.core.make_label()
        label = self.values.replace_label_values_with_variable_values(label)
        return label

    def _sample_range_operators(self) -> Iterator[operators.Operator[core.ranges.Range]]:
        return self.faker.stream_random_items(factory_func=self._make_range_operator, min_size=1, max_size=3)

    def _make_range_operator(self) -> operators.Operator[core.ranges.Range]:
        return self.faker.random_element(elements=frozenset(self._stream_range_operators()))

    def _stream_range_operators(self) -> Iterator[operators.Operator[core.ranges.Range]]:
        yield self._make_switch_operator(make_case=self._make_range)
        yield self._make_return_operator(make_case=self._make_range)

    def _make_range(self) -> core.ranges.Range:
        range_ = self.core.make_range()
        range_ = self.values.replace_range_values_with_variable_values(range_)
        return range_

    def _make_switch_operator(self, make_case: Callable[[], Case]) -> operators.Switch[Case]:
        return operators.Switch(
            ref=self._make_reference(),
            cases=read_only(dict_from_list(self._stream_argument_types(), value_func=lambda _: self._make_return_operator(make_case, max_size=1))),
        )

    def _make_return_operator(self, make_case: Callable[[], Case], max_size: int = 3) -> operators.Return[Case]:
        return operators.Return(
            cases=tuple(self.faker.stream_random_items(make_case, min_size=1, max_size=max_size)),
        )

    def _make_variable_value(self) -> values.Value:
        return self.faker.random_element(elements={
            self.make_variable(),
            self.make_constant(),
        })

    def make_variable(self) -> values.Variable:
        return values.Variable(ref=self._make_reference(), index=self.faker.random_int(min=1, max=5))

    def make_constant(self) -> values.Constant:
        return values.Constant(value=self.core.make_scalar())

    def _make_reference(self):
        return Reference(alias=self.faker.word())

    class Values:
        Case = TypeVar('Case')

        def __init__(self, fakes: Fakes):
            self.fakes = fakes
            self.faker = fakes.faker
            self.label_to_replace_values_func_map = ensure_map_is_complete(core.labels.Label, {
                core.labels.Value: self._replace_value_label_value_with_variable_value,
                core.labels.Badge: as_is,
                core.labels.Empty: as_is,
            })
            self.range_to_replace_values_func_map: Mapping[Type[Range], Callable[[Range], Range]] = ensure_map_is_complete(core.ranges.Range, {
                core.ranges.Between: self._replace_between_range_values_with_variable_values,
                core.ranges.LessThan: self._replace_less_than_range_value_with_variable_value,
                core.ranges.MoreThan: self._replace_more_than_range_value_with_variable_value,
            })

        def replace_label_values_with_variable_values(self, label: core.labels.Label) -> core.labels.Label:
            return self.label_to_replace_values_func_map[type(label)](label)

        def _replace_value_label_value_with_variable_value(self, label: core.labels.Value) -> core.labels.Value:
            return replace(label, value=self.fakes._make_variable_value())

        def replace_range_values_with_variable_values(self, range_: core.ranges.Range) -> core.ranges.Range:
            return self.range_to_replace_values_func_map[type(range_)](range_)

        def _replace_between_range_values_with_variable_values(self, range_: core.ranges.Between) -> core.ranges.Between:
            return replace(range_, min_value=self.fakes._make_variable_value(), max_value=self.fakes._make_variable_value())

        def _replace_less_than_range_value_with_variable_value(self, range_: core.ranges.LessThan) -> core.ranges.LessThan:
            return replace(range_, value=self.fakes._make_variable_value())

        def _replace_more_than_range_value_with_variable_value(self, range_: core.ranges.MoreThan) -> core.ranges.MoreThan:
            return replace(range_, value=self.fakes._make_variable_value())
