from unittest.mock import Mock
from unittest.mock import call
from pytest import fixture

from rmshared import sql
from rmshared.content.taxonomy import core
from rmshared.content.taxonomy.variables import operators
from rmshared.content.taxonomy.variables.sql.compiling.filters import Filters
from rmshared.content.taxonomy.variables.sql.compiling.operators import Operators
from rmshared.content.taxonomy.variables.sql.compiling.variables import Variables


class TestFilters:
    @fixture
    def filters(self, operators_: Operators, delegate: core.sql.compiling.IFilters) -> Filters:
        return Filters(operators_, delegate)

    @fixture
    def operators_(self, variables: Variables) -> Operators:
        return Operators(variables)

    @fixture
    def variables(self) -> Variables:
        return Variables()

    @fixture
    def delegate(self) -> Mock | core.sql.compiling.IFilters:
        return Mock(spec=core.sql.compiling.IFilters)

    def test_it_should_make_tree_from_filter(self, filters: Filters, delegate: Mock | core.sql.compiling.IFilters):
        delegate.make_tree_from_filter = Mock(return_value=self.StubTree('compiled_filter'))
        case_1 = Mock()
        case_2 = Mock()

        return_operator = operators.Return(cases=[case_1, case_2])
        tree = filters.make_tree_from_filter(return_operator)
        compiled = list(tree.compile())

        assert delegate.make_tree_from_filter.call_args_list == [call(case_1), call(case_2)]
        assert compiled == ['compiled_filter', ' ', 'AND', 'compiled_filter']

    class StubTree(sql.compiling.ITree):
        def __init__(self, compiled_output: str):
            self.compiled_output = compiled_output

        def compile(self):
            yield self.compiled_output
