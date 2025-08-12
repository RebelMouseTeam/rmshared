from unittest.mock import Mock
from unittest.mock import call
from pytest import fixture

from rmshared import sql
from rmshared.content.taxonomy import core
from rmshared.content.taxonomy.variables import operators
from rmshared.content.taxonomy.variables.sql.compiling.ranges import Ranges
from rmshared.content.taxonomy.variables.sql.compiling.operators import Operators
from rmshared.content.taxonomy.variables.sql.compiling.variables import Variables


class TestRanges:
    @fixture
    def ranges(self, operators_: Operators, delegate: core.sql.compiling.IRanges) -> Ranges:
        return Ranges(operators_, delegate)

    @fixture
    def operators_(self, variables: Variables) -> Operators:
        return Operators(variables)

    @fixture
    def variables(self) -> Variables:
        return Variables()

    @fixture
    def delegate(self) -> Mock | core.sql.compiling.IRanges:
        return Mock(spec=core.sql.compiling.IRanges)

    def test_it_should_make_tree_from_ranges_with_one_return_operator(self, ranges: Ranges, delegate: Mock | core.sql.compiling.IRanges):
        delegate.make_tree_from_ranges = Mock(return_value=self.StubTree('compiled_ranges'))
        case_1 = Mock()
        matcher = Mock()

        return_operator = operators.Return(cases=[case_1])
        ranges_ = [return_operator]
        tree = ranges.make_tree_from_ranges(ranges_, matcher)
        compiled = list(tree.compile())

        assert delegate.make_tree_from_ranges.call_args_list == [call([case_1], matcher)]
        assert compiled == ['compiled_ranges']

    def test_it_should_make_tree_from_ranges_with_two_return_operators(self, ranges: Ranges, delegate: Mock | core.sql.compiling.IRanges):
        delegate.make_tree_from_ranges = Mock(return_value=self.StubTree('compiled_ranges'))
        case_1 = Mock()
        case_2 = Mock()
        matcher = Mock()

        return_operator_1 = operators.Return(cases=[case_1])
        return_operator_2 = operators.Return(cases=[case_2])
        ranges_ = [return_operator_1, return_operator_2]
        tree = ranges.make_tree_from_ranges(ranges_, matcher)
        compiled = list(tree.compile())

        assert delegate.make_tree_from_ranges.call_args_list == [call([case_1], matcher), call([case_2], matcher)]
        assert compiled == ['(', 'compiled_ranges', 'OR', 'compiled_ranges', ')']

    class StubTree(sql.compiling.ITree):
        def __init__(self, compiled_output: str):
            self.compiled_output = compiled_output

        def compile(self):
            yield self.compiled_output
