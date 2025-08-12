from pytest import fixture

from rmshared.content.taxonomy.variables.abc import Reference
from rmshared.content.taxonomy.variables.sql.compiling.variables import Variables


class TestVariables:
    @fixture
    def variables(self) -> Variables:
        return Variables()

    def test_it_should_resolve_index_pattern(self, variables: Variables):
        ref = Reference(alias='$1')

        result = variables.make_tree_from_reference(ref)
        compiled = list(result.compile())
        assert compiled == ['@@1']

    def test_it_should_resolve_multiple_digit_index(self, variables: Variables):
        ref = Reference(alias='$42')

        result = variables.make_tree_from_reference(ref)
        compiled = list(result.compile())
        assert compiled == ['@@42']

    def test_it_should_resolve_zero_index(self, variables: Variables):
        ref = Reference(alias='$0')
        
        result = variables.make_tree_from_reference(ref)
        compiled = list(result.compile())
        assert compiled == ['@@0']

    def test_it_should_resolve_named_variable(self, variables: Variables):
        ref = Reference(alias='variable_name')
        
        result = variables.make_tree_from_reference(ref)
        compiled = list(result.compile())
        assert compiled == ['@variable_name']

    def test_it_should_resolve_complex_named_variable(self, variables: Variables):
        ref = Reference(alias='some_complex_variable_name_123')
        
        result = variables.make_tree_from_reference(ref)
        compiled = list(result.compile())
        assert compiled == ['@some_complex_variable_name_123']

    def test_it_should_resolve_partial_index_patterns(self, variables: Variables):
        test_cases = [
            ('$a1', '@$a1'),
            ('1$', '@1$'),
            ('$1a', '@$1a'),
            ('a$1', '@a$1'),
        ]
        
        for alias, expected_name in test_cases:
            ref = Reference(alias=alias)
            
            result = variables.make_tree_from_reference(ref)
            compiled = list(result.compile())
            assert compiled == [expected_name]

    def test_it_should_resolve_edge_cases(self, variables: Variables):
        edge_cases = [
            ('', '@'),
            ('@', '@@'),
            ('$', '@$'),
            ('_', '@_'),
            ('123', '@123'),
        ]
        
        for alias, expected_name in edge_cases:
            ref = Reference(alias=alias)
            
            result = variables.make_tree_from_reference(ref)
            compiled = list(result.compile())
            assert compiled == [expected_name]
