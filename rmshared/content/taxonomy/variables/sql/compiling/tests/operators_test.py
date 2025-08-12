from unittest.mock import Mock
from unittest.mock import call
from pytest import fixture

from rmshared import sql

from rmshared.content.taxonomy.variables import arguments
from rmshared.content.taxonomy.variables import operators
from rmshared.content.taxonomy.variables.abc import Reference
from rmshared.content.taxonomy.variables.sql.compiling.abc import IVariables
from rmshared.content.taxonomy.variables.sql.compiling.operators import Operators


class TestOperators:
    @fixture
    def operators_(self, variables: IVariables) -> Operators:
        return Operators(variables)

    @fixture
    def variables(self) -> Mock | IVariables:
        return Mock(spec=IVariables)

    def test_it_should_make_tree_from_switch_operator(self, operators_: Operators, variables: Mock | IVariables):
        make_tree_from_cases_func = Mock(return_value=self.StubTree('compiled_cases'))
        variables.make_tree_from_reference = Mock(return_value=Mock(wraps=self.StubTree(compiled_output='@test_ref')))
        case_1 = Mock()
        case_2 = Mock()

        ref = Reference(alias='test_ref')
        return_operator_1 = operators.Return(cases=[case_1, case_2])
        switch_operator_1 = operators.Switch(ref=ref, cases={arguments.Any: return_operator_1})
        tree_1 = operators_.make_tree_from_operator(switch_operator_1, make_tree_from_cases_func)
        compiled_1 = list(tree_1.compile())

        return_operator_2 = operators.Return(cases=[case_1])
        return_operator_3 = operators.Return(cases=[])
        switch_operator_2 = operators.Switch(ref=ref, cases={arguments.Value: return_operator_2, arguments.Any: return_operator_3})
        tree_2 = operators_.make_tree_from_operator(switch_operator_2, make_tree_from_cases_func)
        compiled_2 = list(tree_2.compile())

        return_operator_4 = operators.Return(cases=[case_2])
        return_operator_5 = operators.Return(cases=[case_1])
        switch_operator_3 = operators.Switch(ref=ref, cases={arguments.Value: return_operator_4, arguments.Any: return_operator_5})
        tree_3 = operators_.make_tree_from_operator(switch_operator_3, make_tree_from_cases_func)
        compiled_3 = list(tree_3.compile())

        assert make_tree_from_cases_func.call_args_list == [
            call([case_1, case_2]),
            call([case_1]),
            call([case_2]),
            call([case_1])
        ]
        assert compiled_1 == ['compiled_cases', 'IF', '@test_ref', 'IS NULL']
        assert compiled_2 == ['compiled_cases', 'IF', '@test_ref', 'IS NOT NULL']
        assert compiled_3 == ['compiled_cases', 'IF', '@test_ref', 'IS NOT NULL', 'OTHERWISE', 'compiled_cases']

    def test_it_should_make_tree_from_return_operator(self, operators_: Operators):
        make_tree_from_cases_func = Mock(return_value=self.StubTree('compiled_cases'))
        case_1 = Mock()
        case_2 = Mock()

        return_operator = operators.Return(cases=[case_1, case_2])
        tree = operators_.make_tree_from_operator(return_operator, make_tree_from_cases_func)
        compiled = list(tree.compile())

        assert make_tree_from_cases_func.call_args_list == [call([case_1, case_2])]
        assert compiled == ['compiled_cases']

    class StubTree(sql.compiling.ITree):
        def __init__(self, compiled_output: str):
            self.compiled_output = compiled_output

        def compile(self):
            yield self.compiled_output
