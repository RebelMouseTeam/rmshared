from unittest.mock import Mock
from unittest.mock import call
from pytest import fixture

from rmshared import sql
from rmshared.content.taxonomy import core
from rmshared.content.taxonomy.variables import values
from rmshared.content.taxonomy.variables.abc import Reference
from rmshared.content.taxonomy.variables.sql.compiling.values import Values
from rmshared.content.taxonomy.variables.sql.compiling.variables import Variables


class TestValues:
    @fixture
    def values_(self, variables: Variables, delegate: core.sql.compiling.IValues) -> Values:
        return Values(variables, delegate)

    @fixture
    def variables(self) -> Variables:
        return Variables()

    @fixture
    def delegate(self) -> Mock | core.sql.compiling.IValues:
        return Mock(spec=core.sql.compiling.IValues)

    def test_it_should_make_tree_from_constant_value(self, values_: Values, delegate: Mock | core.sql.compiling.IValues):
        delegate.make_tree_from_value = Mock(return_value=self.StubTree('compiled_constant'))

        constant_value = values.Constant(value='test_value')
        tree = values_.make_tree_from_value(constant_value)
        compiled = list(tree.compile())

        assert delegate.make_tree_from_value.call_args_list == [call('test_value')]
        assert compiled == ['compiled_constant']

    def test_it_should_make_tree_from_variable_value(self, values_: Values):
        ref = Reference(alias='test_var')
        variable_value = values.Variable(ref=ref, index=1)
        tree = values_.make_tree_from_value(variable_value)
        compiled = list(tree.compile())

        assert compiled == ['@test_var']

    def test_it_should_make_tree_from_variable_value_with_index(self, values_: Values):
        ref = Reference(alias='test_var')
        variable_value = values.Variable(ref=ref, index=2)
        tree = values_.make_tree_from_value(variable_value)
        compiled = list(tree.compile())

        assert compiled == ['@test_var', '[', '2', ']']

    class StubTree(sql.compiling.ITree):
        def __init__(self, compiled_output: str):
            self.compiled_output = compiled_output

        def compile(self):
            yield self.compiled_output
