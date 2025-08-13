from unittest.mock import Mock
from unittest.mock import call
from pytest import fixture

from rmshared import sql
from rmshared.content.taxonomy import core
from rmshared.content.taxonomy.variables import operators
from rmshared.content.taxonomy.variables import arguments
from rmshared.content.taxonomy.variables.abc import Reference
from rmshared.content.taxonomy.variables.sql.compiling.labels import Labels
from rmshared.content.taxonomy.variables.sql.compiling.operators import Operators
from rmshared.content.taxonomy.variables.sql.compiling.variables import Variables


class TestLabels:
    @fixture
    def labels(self, operators_: Operators, delegate: core.sql.compiling.ILabels) -> Labels:
        return Labels(operators_, delegate)

    @fixture
    def operators_(self, variables: Variables) -> Operators:
        return Operators(variables)

    @fixture
    def variables(self) -> Variables:
        return Variables()

    @fixture
    def delegate(self) -> Mock | core.sql.compiling.ILabels:
        return Mock(spec=core.sql.compiling.ILabels)

    def test_it_should_make_tree_from_labels_with_one_return_operator(self, labels: Labels, delegate: Mock | core.sql.compiling.ILabels):
        delegate.make_tree_from_labels = Mock(return_value=self.StubTree('compiled_labels'))
        case_1 = Mock()
        matcher = Mock()

        return_operator = operators.Return(cases=[case_1])
        labels_ = [return_operator]
        tree = labels.make_tree_from_labels(labels_, matcher)
        compiled = list(tree.compile())

        assert delegate.make_tree_from_labels.call_args_list == [call([case_1], matcher)]
        assert compiled == ['compiled_labels']

    def test_it_should_make_tree_from_labels_with_two_return_operators(self, labels: Labels, delegate: Mock | core.sql.compiling.ILabels):
        delegate.make_tree_from_labels = Mock(return_value=self.StubTree('compiled_labels'))
        case_1 = Mock()
        case_2 = Mock()
        matcher = Mock()

        return_operator_1 = operators.Return(cases=[case_1])
        return_operator_2 = operators.Return(cases=[case_2])
        labels_ = [return_operator_1, return_operator_2]
        tree = labels.make_tree_from_labels(labels_, matcher)
        compiled = list(tree.compile())

        assert delegate.make_tree_from_labels.call_args_list == [call((case_1, case_2), matcher)]
        assert compiled == ['compiled_labels']

    def test_it_should_make_tree_from_labels_with_mixed_operators(self, labels: Labels, delegate: Mock | core.sql.compiling.ILabels):
        delegate.make_tree_from_labels = Mock(return_value=self.StubTree('compiled_labels'))
        case_1 = Mock()
        case_2 = Mock()
        case_3 = Mock()
        case_4 = Mock()
        case_5 = Mock()
        case_6 = Mock()
        case_7 = Mock()
        case_8 = Mock()
        case_9 = Mock()
        matcher = Mock()

        return_operator_1 = operators.Return(cases=[case_1])
        return_operator_2 = operators.Return(cases=[case_2])
        switch_operator_1 = operators.Switch(ref=Reference(alias='var1'), cases={
            arguments.Any: operators.Return(cases=[]),
            arguments.Value: operators.Return(cases=[case_3]),
        })
        switch_operator_2 = operators.Switch(ref=Reference(alias='var2'), cases={
            arguments.Any: operators.Return(cases=[case_4]),
            arguments.Value: operators.Return(cases=[]),
        })
        return_operator_3 = operators.Return(cases=[case_5])
        return_operator_4 = operators.Return(cases=[case_6])
        switch_operator_3 = operators.Switch(ref=Reference(alias='var3'), cases={
            arguments.Any: operators.Return(cases=[case_8]),
            arguments.Value: operators.Return(cases=[case_7]),
        })
        return_operator_5 = operators.Return(cases=[case_9])
        labels_ = [
            return_operator_1,
            return_operator_2,
            switch_operator_1,
            switch_operator_2,
            return_operator_3,
            return_operator_4,
            switch_operator_3,
            return_operator_5,
        ]
        tree = labels.make_tree_from_labels(labels_, matcher)
        compiled = list(tree.compile())

        assert delegate.make_tree_from_labels.call_args_list == [
            call((case_1, case_2), matcher),
            call([case_3], matcher),
            call([case_4], matcher),
            call((case_5, case_6), matcher),
            call([case_7], matcher),
            call([case_8], matcher),
            call([case_9], matcher)
        ]
        assert compiled == [
            '(',
            'compiled_labels',
            'OR', 'compiled_labels', 'IF', '@var1', 'IS NOT NULL',
            'OR', 'compiled_labels', 'IF', '@var2', 'IS NULL',
            'OR', 'compiled_labels',
            'OR', 'compiled_labels', 'IF', '@var3', 'IS NOT NULL', 'OTHERWISE', 'compiled_labels',
            'OR', 'compiled_labels',
            ')'
        ]

    class StubTree(sql.compiling.ITree):
        def __init__(self, compiled_output: str):
            self.compiled_output = compiled_output

        def compile(self):
            yield self.compiled_output
