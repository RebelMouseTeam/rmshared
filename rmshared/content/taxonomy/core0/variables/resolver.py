from dataclasses import replace
from itertools import chain
from typing import Iterable
from typing import Iterator

from rmshared.content.taxonomy.core0 import filters as core0_filters
from rmshared.content.taxonomy.core0 import labels as core0_labels
from rmshared.content.taxonomy.core0 import ranges as core0_ranges
from rmshared.content.taxonomy.core0.abc import Filter
from rmshared.content.taxonomy.core0.abc import Label
from rmshared.content.taxonomy.core0.abc import Range
from rmshared.content.taxonomy.core0.abc import Scalar

from rmshared.content.taxonomy.core0.variables import filters
from rmshared.content.taxonomy.core0.variables import labels
from rmshared.content.taxonomy.core0.variables import ranges
from rmshared.content.taxonomy.core0.variables.abc import Constant
from rmshared.content.taxonomy.core0.variables.abc import Variable
from rmshared.content.taxonomy.core0.variables.abc import IResolver


class Resolver(IResolver):
    def dereference_filters(self, filters_, arguments):
        return self.ConfiguredResolver(arguments).dereference_filters(filters_)

    class ConfiguredResolver:
        def __init__(self, arguments_: IResolver.IArguments):
            self.arguments = arguments_

        def dereference_filters(self, filters_: Iterable[Filter]) -> Iterator[Filter]:
            return chain.from_iterable(map(self._dereference_filter, filters_))

        def _dereference_filter(self, filter_: Filter) -> Iterator[Filter]:
            if isinstance(filter_, filters.Switch):
                return self._dereference_switch_filter(filter_)
            elif isinstance(filter_, (core0_filters.AnyLabel, core0_filters.NoLabels)):
                return [self._dereference_labels_filter(filter_)]
            elif isinstance(filter_, (core0_filters.AnyRange, core0_filters.NoRanges)):
                return [self._dereference_ranges_filter(filter_)]
            else:
                raise NotImplementedError(['dereference_filter', filter_])

        def _dereference_switch_filter(self, filter_: filters.Switch) -> Iterator[Filter]:
            argument = self.arguments.get_argument(filter_.ref.alias)
            return chain.from_iterable(map(self._dereference_filter, filter_.cases.cases.get(type(argument), [])))

        def _dereference_labels_filter(self, filter_: core0_filters.AnyLabel | core0_filters.NoLabels) -> Filter:
            return replace(filter_, labels=tuple(chain.from_iterable(map(self._dereference_label, filter_.labels))))

        def _dereference_ranges_filter(self, filter_: core0_filters.AnyRange | core0_filters.NoRanges) -> Filter:
            return replace(filter_, ranges=tuple(chain.from_iterable(map(self._dereference_range, filter_.ranges))))

        def _dereference_label(self, label_: Label) -> Iterator[Label]:
            if isinstance(label_, labels.Switch):
                return self._dereference_switch_label(label_)
            elif isinstance(label_, labels.Value):
                return [self._dereference_value_label(label_)]
            else:
                return [label_]

        def _dereference_switch_label(self, label_: labels.Switch) -> Iterator[Label]:
            argument = self.arguments.get_argument(label_.ref.alias)
            return chain.from_iterable(map(self._dereference_label, label_.cases.cases.get(type(argument), [])))

        def _dereference_value_label(self, label_: labels.Value) -> Label:
            value = self.arguments.get_value(label_.value.ref.alias, label_.value.index)
            return core0_labels.Value(field=label_.field, value=value)

        def _dereference_range(self, range_: Range) -> Iterator[Range]:
            if isinstance(range_, ranges.Switch):
                return self._dereference_switch_range(range_)
            elif isinstance(range_, ranges.LessThan):
                return [self._dereference_less_than_range(range_)]
            elif isinstance(range_, ranges.MoreThan):
                return [self._dereference_more_than_range(range_)]
            elif isinstance(range_, ranges.Between):
                return [self._dereference_between_range(range_)]
            else:
                return [range_]

        def _dereference_switch_range(self, range_: ranges.Switch) -> Iterator[Range]:
            argument = self.arguments.get_argument(range_.ref.alias)
            return chain.from_iterable(map(self._dereference_range, range_.cases.cases.get(type(argument), [])))

        def _dereference_less_than_range(self, range_: ranges.LessThan) -> Range:
            value = self.arguments.get_value(range_.value.ref.alias, range_.value.index)
            return core0_ranges.LessThan(field=range_.field, value=value)

        def _dereference_more_than_range(self, range_: ranges.MoreThan) -> Range:
            value = self.arguments.get_value(range_.value.ref.alias, range_.value.index)
            return core0_ranges.MoreThan(field=range_.field, value=value)

        def _dereference_between_range(self, range_: ranges.Between) -> Range:
            min_value = self._dereference_variable_or_constant(range_.min_value)
            max_value = self._dereference_variable_or_constant(range_.max_value)
            return core0_ranges.Between(field=range_.field, min_value=min_value, max_value=max_value)

        def _dereference_variable_or_constant(self, value: Variable | Constant) -> Scalar:
            if isinstance(value, Variable):
                return self.arguments.get_value(value.ref.alias, value.index)
            elif isinstance(value, Constant):
                return value.value
            else:
                raise NotImplementedError(['dereference_variable_or_constant', value])
