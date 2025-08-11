from __future__ import annotations

from abc import ABCMeta
from abc import abstractmethod
from collections import defaultdict
from collections.abc import Callable
from collections.abc import Iterable
from collections.abc import Iterator
from collections.abc import Mapping
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Generic
from typing import Type
from typing import TypeVar

from rmshared.tools import ensure_map_is_complete

from rmshared.sql import compiling

from rmshared.content.taxonomy.core import fields
from rmshared.content.taxonomy.core import ranges
from rmshared.content.taxonomy.core import traversal
from rmshared.content.taxonomy.core.sql.compiling.abc import IFields
from rmshared.content.taxonomy.core.sql.compiling.abc import IValues
from rmshared.content.taxonomy.core.sql.compiling.abc import IRanges

F = TypeVar('F', bound=fields.Field)
R = TypeVar('R', bound=ranges.Range)


class Ranges(IRanges[ranges.Range]):
    def __init__(self, fields_: IFields, values_: IValues, traversal_: traversal.IRanges[R]):
        self.fields = fields_
        self.values = values_
        self.aggregator = self.Aggregator(traversal_)
        self.matcher_to_strategy_map: Mapping[Type[IRanges.Matcher], Ranges.IMatchStrategy] = ensure_map_is_complete(IRanges.Matcher, {
            IRanges.Match: self.MatchStrategy(),
            IRanges.MatchNot: self.MatchNotStrategy(),
        })

    def make_tree_from_ranges(self, ranges_: Iterable[ranges.Range], matcher):
        groups = tuple(self.aggregator.aggregate(ranges_))
        strategy = self.matcher_to_strategy_map[type(matcher)]
        operations = self.Operations(self.fields, self.values, strategy)
        expressions = tuple(map(operations.make_tree_from_group, groups))
        return strategy.connect_expressions(expressions)

    class Aggregator:
        def __init__(self, traversal_: traversal.IRanges[R]):
            self.traversal = traversal_

        def aggregate(self, ranges_: Iterable[R]) -> Iterator[Group[R]]:
            visitor = self.Visitor()
            self.traversal.traverse_ranges(ranges_, visitor)
            for field, ranges_ in visitor.field_to_ranges_map.items():
                yield self.Group(field=field, ranges=tuple(ranges_))

        class Visitor(traversal.visitors.IRanges):
            def __init__(self):
                self.field_to_ranges_map: dict[fields.Field, list[ranges.Range]] = defaultdict(list)

            def visit_range(self, range_: ranges.Range):
                self.field_to_ranges_map[range_.field].append(range_)

        @dataclass(frozen=True)
        class Group(Generic[R]):
            field: fields.Field
            ranges: Sequence[R]

    class Operations:
        def __init__(self, fields_: IFields, values_: IValues, strategy: Ranges.IMatchStrategy):
            self.fields = fields_
            self.values = values_
            self.strategy = strategy
            self.range_to_make_tree_func_map: Mapping[Type[R], Callable[[R], compiling.ITree]] = ensure_map_is_complete(ranges.Range, {
                ranges.Between: self._make_tree_from_between_range,
                ranges.LessThan: self._make_tree_from_less_than_range,
                ranges.MoreThan: self._make_tree_from_more_than_range,
            })

        def make_tree_from_group(self, group: Ranges.Aggregator.Group[R]) -> compiling.ITree:
            expressions = tuple(map(self._make_tree_from_range, group.ranges))
            return self.strategy.connect_expressions(expressions)

        def _make_tree_from_range(self, range_: R) -> compiling.ITree:
            return self.range_to_make_tree_func_map[type(range_)](range_)

        def _make_tree_from_between_range(self, range_: ranges.Between) -> compiling.ITree:
            operations = self.fields.make_field_operations(range_.field)
            min_value = self.values.make_tree_from_value(range_.min_value)
            max_value = self.values.make_tree_from_value(range_.max_value)
            return self.strategy.make_between_operation(operations, min_value, max_value)

        def _make_tree_from_less_than_range(self, range_: ranges.LessThan) -> compiling.ITree:
            operations = self.fields.make_field_operations(range_.field)
            value = self.values.make_tree_from_value(range_.value)
            return self.strategy.make_less_than_operation(operations, value)

        def _make_tree_from_more_than_range(self, range_: ranges.MoreThan) -> compiling.ITree:
            operations = self.fields.make_field_operations(range_.field)
            value = self.values.make_tree_from_value(range_.value)
            return self.strategy.make_more_than_operation(operations, value)

    class IMatchStrategy(metaclass=ABCMeta):
        @abstractmethod
        def make_between_operation(self, operations: IFields.IOperations, min_value: compiling.ITree, max_value: compiling.ITree) -> compiling.ITree:
            ...

        @abstractmethod
        def make_less_than_operation(self, operations: IFields.IOperations, value: compiling.ITree) -> compiling.ITree:
            ...

        @abstractmethod
        def make_more_than_operation(self, operations: IFields.IOperations, value: compiling.ITree) -> compiling.ITree:
            ...

        @abstractmethod
        def connect_expressions(self, expressions: Sequence[compiling.ITree]) -> compiling.ITree:
            ...

    class MatchStrategy(IMatchStrategy):
        def make_between_operation(self, operations, min_value, max_value):
            return operations.make_between_operation(min_value, max_value)

        def make_less_than_operation(self, operations, value):
            return operations.make_less_than_operation(value)

        def make_more_than_operation(self, operations, value):
            return operations.make_more_than_operation(value)

        def connect_expressions(self, expressions):
            return compiling.logical.Disjunction(expressions, parenthesis='()')

    class MatchNotStrategy(IMatchStrategy):
        def make_between_operation(self, operations, min_value, max_value):
            return operations.make_not_between_operation(min_value, max_value)

        def make_less_than_operation(self, operations, value):
            return operations.make_more_than_or_equal_operation(value)

        def make_more_than_operation(self, operations, value):
            return operations.make_less_than_or_equal_operation(value)

        def connect_expressions(self, expressions):
            return compiling.logical.Conjunction(expressions)
