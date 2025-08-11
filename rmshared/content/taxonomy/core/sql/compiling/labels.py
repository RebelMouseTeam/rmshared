from __future__ import annotations

from abc import ABCMeta
from abc import abstractmethod
from collections import defaultdict
from collections.abc import Iterable
from collections.abc import Iterator
from collections.abc import Mapping
from collections.abc import Sequence
from dataclasses import dataclass
from operator import attrgetter
from typing import Generic
from typing import Type
from typing import TypeVar

from rmshared.tools import ensure_map_is_complete

from rmshared.sql import compiling

from rmshared.content.taxonomy.core import fields
from rmshared.content.taxonomy.core import labels
from rmshared.content.taxonomy.core import traversal
from rmshared.content.taxonomy.core.sql.compiling.abc import IFields
from rmshared.content.taxonomy.core.sql.compiling.abc import IValues
from rmshared.content.taxonomy.core.sql.compiling.abc import ILabels

F = TypeVar('F', bound=fields.Field)
L = TypeVar('L', bound=labels.Label)


class Labels(ILabels[labels.Label]):
    def __init__(self, fields_: IFields, values_: IValues, traversal_: traversal.ILabels[L]):
        self.fields = fields_
        self.values = values_
        self.aggregator = self.Aggregator(traversal_)
        self.matcher_to_strategy_map: Mapping[Type[ILabels.Matcher], Labels.IMatchStrategy] = ensure_map_is_complete(ILabels.Matcher, {
            ILabels.Match: self.MatchStrategy(),
            ILabels.MatchNot: self.MatchNotStrategy(),
        })

    def make_tree_from_labels(self, labels_: Iterable[labels.Label], matcher):
        groups = tuple(self.aggregator.aggregate(labels_))
        strategy = self.matcher_to_strategy_map[type(matcher)]
        operations = self.Operations(self.fields, self.values, strategy)
        expressions = tuple(map(operations.make_tree_from_group, groups))
        return strategy.connect_expressions(expressions)

    class Aggregator:
        def __init__(self, traversal_: traversal.ILabels[L]):
            self.traversal = traversal_

        def aggregate(self, labels_: Iterable[L]) -> Iterator[Group[L]]:
            visitor = self.Visitor()
            self.traversal.traverse_labels(labels_, visitor)
            for (field, label_type), labels_ in visitor.field_and_label_type_to_labels_map.items():
                yield self.Group(field=field, label_type=label_type, labels=tuple(labels_))

        class Visitor(traversal.visitors.ILabels):
            def __init__(self):
                self.field_and_label_type_to_labels_map: dict[tuple[F, Type[L]], list[L]] = defaultdict(list)

            def visit_label(self, label: labels.Label):
                self.field_and_label_type_to_labels_map[label.field, type(label)].append(label)

        @dataclass(frozen=True)
        class Group(Generic[L]):
            field: fields.Field
            label_type: Type[L]
            labels: Sequence[L]

    class Operations:
        def __init__(self, fields_: IFields, values_: IValues, strategy: Labels.IMatchStrategy):
            self.fields = fields_
            self.values = values_
            self.strategy = strategy
            self.label_to_make_tree_func_map: Mapping[Type[L], compiling.MakeTreeFunc[[F, Sequence[L]]]] = ensure_map_is_complete(labels.Label, {
                labels.Badge: self._make_tree_from_badge_labels,
                labels.Empty: self._make_tree_from_empty_labels,
                labels.Value: self._make_tree_from_value_labels,
            })

        def make_tree_from_group(self, group: Labels.Aggregator.Group[L]) -> compiling.ITree:
            return self.label_to_make_tree_func_map[group.label_type](group.field, group.labels)

        def _make_tree_from_badge_labels(self, field: fields.Field, labels_: Sequence[labels.Badge]) -> compiling.ITree:
            assert len(labels_) == 1, 'Badge labels should be unique per field'
            operations = self.fields.make_field_operations(field)
            return self.strategy.make_match_badge_operation(operations)

        def _make_tree_from_empty_labels(self, field: fields.Field, labels_: Sequence[labels.Empty]) -> compiling.ITree:
            assert len(labels_) == 1, 'Empty labels should be unique per field'
            operations = self.fields.make_field_operations(field)
            return self.strategy.make_match_empty_operation(operations)

        def _make_tree_from_value_labels(self, field: fields.Field, labels_: Sequence[labels.Value]) -> compiling.ITree:
            assert len(labels_) >= 1, 'Value labels should not be empty'
            operations = self.fields.make_field_operations(field)
            values = tuple(map(self.values.make_tree_from_value, map(attrgetter('value'), labels_)))
            return self._make_tree_from_values(operations, values)

        def _make_tree_from_values(self, operations: IFields.IOperations, values: Sequence[compiling.ITree]) -> compiling.ITree:
            if len(values) == 1:
                return self.strategy.make_match_one_value_operation(operations, expression=values[0])
            else:
                expression = compiling.utils.Chain.from_iterable(values)
                expression = compiling.utils.Compacted(expression, compiling.compact.with_comma)
                expression = compiling.utils.Wrapped(expression, parentheses='()')
                expression = compiling.utils.Compacted(expression, compiling.compact.with_nothing)
                return self.strategy.make_match_any_value_operation(operations, expression=expression)

    class IMatchStrategy(metaclass=ABCMeta):
        @abstractmethod
        def make_match_badge_operation(self, operations: IFields.IOperations) -> compiling.ITree:
            ...

        @abstractmethod
        def make_match_empty_operation(self, operations: IFields.IOperations) -> compiling.ITree:
            ...

        @abstractmethod
        def make_match_one_value_operation(self, operations: IFields.IOperations, expression: compiling.ITree) -> compiling.ITree:
            ...

        @abstractmethod
        def make_match_any_value_operation(self, operations: IFields.IOperations, expression: compiling.ITree) -> compiling.ITree:
            ...

        @abstractmethod
        def connect_expressions(self, expressions: Sequence[compiling.ITree]) -> compiling.ITree:
            ...

    class MatchStrategy(IMatchStrategy):
        def make_match_badge_operation(self, operations):
            return operations.make_match_badge_operation()

        def make_match_empty_operation(self, operations):
            return operations.make_match_empty_operation()

        def make_match_one_value_operation(self, operations, expression):
            return operations.make_match_one_value_operation(expression)

        def make_match_any_value_operation(self, operations, expression):
            return operations.make_match_any_value_operation(expression)

        def connect_expressions(self, expressions):
            return compiling.logical.Disjunction(expressions, parenthesis='()')

    class MatchNotStrategy(IMatchStrategy):
        def make_match_badge_operation(self, operations):
            return operations.make_does_not_match_badge_operation()

        def make_match_empty_operation(self, operations):
            return operations.make_does_not_match_empty_operation()

        def make_match_one_value_operation(self, operations, expression):
            return operations.make_does_not_match_one_value_operation(expression)

        def make_match_any_value_operation(self, operations, expression):
            return operations.make_does_not_match_any_value_operation(expression)

        def connect_expressions(self, expressions):
            return compiling.logical.Conjunction(expressions)
