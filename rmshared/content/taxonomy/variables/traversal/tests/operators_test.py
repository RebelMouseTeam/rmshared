from contextlib import contextmanager

from pytest import fixture

from rmshared.content.taxonomy.variables import arguments
from rmshared.content.taxonomy.variables import operators
from rmshared.content.taxonomy.variables.abc import Reference
from rmshared.content.taxonomy.variables.fakes import Fakes
from rmshared.content.taxonomy.variables.traversal import visitors
from rmshared.content.taxonomy.variables.traversal.operators import Operators


class TestOperators:
    @fixture
    def traverser(self) -> Operators:
        return Operators()

    @fixture
    def fakes(self):
        return Fakes()

    def test_it_should_traverse_operators(self, fakes: Fakes, traverser: Operators):
        class Visitor(visitors.IOperators, visitors.IArguments, Operators.IVisitor[object]):
            def __init__(self):
                self.visits = []

            def visit_operator(self, operator):
                self.visits.append(('visit_operator', operator))

            def visit_argument(self, argument):
                self.visits.append(('visit_argument', argument))

            def traverse_cases(self, cases):
                self.visits.append(('traverse_cases', cases))

        case_1 = object()
        case_2 = object()
        case_3 = object()
        operator_1 = operators.Return(cases=(case_1,))
        operator_2 = operators.Return(cases=(case_2,))
        operator_3 = operators.Return(cases=(case_3,))
        operator_4 = operators.Switch(ref=Reference(alias='variable'), cases={
            arguments.Any: operator_2,
            arguments.Value: operator_3,
        })

        visitor = Visitor()
        traverser.traverse_operators(operators_=[operator_1, operator_4], visitor=visitor)

        assert visitor.visits == [
            ('visit_operator', operator_1),
            ('traverse_cases', (case_1,)),
            ('visit_operator', operator_4),
            ('visit_argument', arguments.Any),
            ('visit_operator', operator_2),
            ('traverse_cases', (case_2,)),
            ('visit_argument', arguments.Value),
            ('visit_operator', operator_3),
            ('traverse_cases', (case_3,)),
        ]

    def test_it_should_traverse_operators_with_context_manager(self, fakes: Fakes, traverser: Operators):
        class Visitor(visitors.IOperators, visitors.IArguments, Operators.IVisitor[object]):
            def __init__(self):
                self.visits = []

            @contextmanager
            def visit_operator(self, operator):
                self.visits.append(('enter_operator', operator))
                yield
                self.visits.append(('leave_operator', operator))

            def visit_argument(self, argument):
                self.visits.append(('visit_argument', argument))

            def traverse_cases(self, cases):
                self.visits.append(('traverse_cases', cases))

        case_1 = object()
        case_2 = object()
        case_3 = object()
        operator_1 = operators.Return(cases=(case_1,))
        operator_2 = operators.Return(cases=(case_2,))
        operator_3 = operators.Return(cases=(case_3,))
        operator_4 = operators.Switch(ref=Reference(alias='variable'), cases={
            arguments.Any: operator_2,
            arguments.Value: operator_3,
        })

        visitor = Visitor()
        traverser.traverse_operators(operators_=[operator_1, operator_4], visitor=visitor)

        assert visitor.visits == [
            ('enter_operator', operator_1),
            ('traverse_cases', (case_1,)),
            ('leave_operator', operator_1),
            ('enter_operator', operator_4),
            ('visit_argument', arguments.Any),
            ('enter_operator', operator_2),
            ('traverse_cases', (case_2,)),
            ('leave_operator', operator_2),
            ('visit_argument', arguments.Value),
            ('enter_operator', operator_3),
            ('traverse_cases', (case_3,)),
            ('leave_operator', operator_3),
            ('leave_operator', operator_4),
        ]
