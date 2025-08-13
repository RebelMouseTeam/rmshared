from pytest import raises
from pytest import fixture

from rmshared.content.taxonomy.core.sql.compiling.values import Values


class TestValues:
    @fixture
    def values(self) -> Values:
        return Values()

    def test_it_should_make_tree_from_string_value(self, values: Values):
        string_value = 'test_string'
        tree = values.make_tree_from_value(string_value)
        compiled = list(tree.compile())

        assert compiled == ["'test_string'"]

    def test_it_should_make_tree_from_string_value_with_quotes(self, values: Values):
        string_value = "test's string"
        tree = values.make_tree_from_value(string_value)
        compiled = list(tree.compile())

        assert compiled == ["'test\\'s string'"]

    def test_it_should_make_tree_from_int_value(self, values: Values):
        int_value = 42
        tree = values.make_tree_from_value(int_value)
        compiled = list(tree.compile())

        assert compiled == ['42']

    def test_it_should_make_tree_from_negative_int_value(self, values: Values):
        int_value = -123
        tree = values.make_tree_from_value(int_value)
        compiled = list(tree.compile())

        assert compiled == ['-123']

    def test_it_should_make_tree_from_float_value(self, values: Values):
        float_value = 3.14
        tree = values.make_tree_from_value(float_value)
        compiled = list(tree.compile())

        assert compiled == ['3.14']

    def test_it_should_make_tree_from_negative_float_value(self, values: Values):
        float_value = -2.71
        tree = values.make_tree_from_value(float_value)
        compiled = list(tree.compile())

        assert compiled == ['-2.71']

    def test_it_should_make_tree_from_zero_int_value(self, values: Values):
        int_value = 0

        tree = values.make_tree_from_value(int_value)
        compiled = list(tree.compile())

        assert compiled == ['0']

    def test_it_should_make_tree_from_zero_float_value(self, values: Values):
        float_value = 0.0

        tree = values.make_tree_from_value(float_value)
        compiled = list(tree.compile())

        assert compiled == ['0.0']

    def test_it_should_raise_error_for_boolean_value(self, values: Values):
        boolean_value = True

        with raises(KeyError):
            values.make_tree_from_value(boolean_value)
