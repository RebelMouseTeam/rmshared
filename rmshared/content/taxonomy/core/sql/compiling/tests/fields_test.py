from unittest.mock import Mock
from unittest.mock import call
from pytest import fixture

from rmshared import sql
from rmshared.content.taxonomy.core import fields
from rmshared.content.taxonomy.core.sql.compiling.abc import IDescriptors
from rmshared.content.taxonomy.core.sql.compiling.fields import Fields


class TestFields:
    @fixture
    def fields_(self, descriptors: IDescriptors) -> Fields:
        return Fields(descriptors)

    @fixture
    def descriptors(self) -> Mock | IDescriptors:
        return Mock(spec=IDescriptors)

    def test_it_should_make_tree_from_system_field(self, fields_: Fields, descriptors: Mock | IDescriptors):
        descriptors.get_field_alias = Mock(return_value='posts.title')

        system_field = fields.System(name='title')
        tree = fields_.make_tree_from_field(system_field)
        compiled = list(tree.compile())

        assert compiled == ['posts.title']
        assert descriptors.get_field_alias.call_args_list == [call(system_field)]

    def test_it_should_make_tree_from_custom_field(self, fields_: Fields):
        custom_field = fields.Custom(name='extras', path='category.priority')
        tree = fields_.make_tree_from_field(custom_field)
        compiled = list(tree.compile())

        assert compiled == ["CUSTOM_FIELD('category.priority')"]

    def test_it_should_make_tree_from_custom_field_with_nested_path(self, fields_: Fields):
        custom_field = fields.Custom(name='extras', path='metadata.section.category')
        tree = fields_.make_tree_from_field(custom_field)
        compiled = list(tree.compile())

        assert compiled == ["CUSTOM_FIELD('metadata.section.category')"]

    def test_it_should_make_tree_from_custom_field_with_simple_path(self, fields_: Fields):
        custom_field = fields.Custom(name='data', path='priority')
        tree = fields_.make_tree_from_field(custom_field)
        compiled = list(tree.compile())

        assert compiled == ["CUSTOM_FIELD('priority')"]

    def test_it_should_make_badge_operations_that_compile_correctly(self, fields_: Fields, descriptors: Mock | IDescriptors):
        descriptors.get_field_alias = Mock(return_value='posts.is_featured')
        descriptors.is_badge_field = Mock(return_value=True)

        system_field = fields.System(name='is_featured')
        operations = fields_.make_field_operations(system_field)
        match_tree = operations.make_match_badge_operation()
        not_match_tree = operations.make_does_not_match_badge_operation()

        assert list(match_tree.compile()) == ['posts.is_featured']
        assert list(not_match_tree.compile()) == ['NOT', 'posts.is_featured']
        assert descriptors.is_badge_field.call_args_list == [call(system_field)]
        assert descriptors.get_field_alias.call_args_list == [call(system_field)]

    def test_it_should_make_single_value_operations_that_compile_correctly(self, fields_: Fields, descriptors: Mock | IDescriptors):
        descriptors.get_field_alias = Mock(return_value='posts.status')
        descriptors.is_badge_field = Mock(return_value=False)
        descriptors.is_multi_value_field = Mock(return_value=False)
        descriptors.is_single_value_field = Mock(return_value=True)
        value_tree = self.StubTree(compiled_output='published')

        system_field = fields.System(name='status')
        operations = fields_.make_field_operations(system_field)
        empty_tree = operations.make_match_empty_operation()
        not_empty_tree = operations.make_does_not_match_empty_operation()
        equal_tree = operations.make_match_one_value_operation(value_tree)
        not_equal_tree = operations.make_does_not_match_one_value_operation(value_tree)
        any_value_tree = operations.make_match_any_value_operation(value_tree)
        not_any_value_tree = operations.make_does_not_match_any_value_operation(value_tree)

        assert list(empty_tree.compile()) == ['posts.status', 'IS NULL']
        assert list(not_empty_tree.compile()) == ['posts.status', 'IS NOT NULL']
        assert list(equal_tree.compile()) == ['posts.status', 'IS', 'published']
        assert list(not_equal_tree.compile()) == ['posts.status', 'IS NOT', 'published']
        assert list(any_value_tree.compile()) == ['posts.status', 'IN', 'published']
        assert list(not_any_value_tree.compile()) == ['posts.status', 'NOT IN', 'published']
        assert descriptors.is_badge_field.call_args_list == [call(system_field)]
        assert descriptors.is_multi_value_field.call_args_list == [call(system_field)]
        assert descriptors.is_single_value_field.call_args_list == [call(system_field)]
        assert descriptors.get_field_alias.call_args_list == [call(system_field)]

    def test_it_should_make_multi_value_operations_that_compile_correctly(self, fields_: Fields, descriptors: Mock | IDescriptors):
        descriptors.get_field_alias = Mock(return_value='posts.tags')
        descriptors.is_badge_field = Mock(return_value=False)
        descriptors.is_multi_value_field = Mock(return_value=True)
        value_tree = self.StubTree(compiled_output='sports')

        system_field = fields.System(name='tags')
        operations = fields_.make_field_operations(system_field)
        empty_tree = operations.make_match_empty_operation()
        not_empty_tree = operations.make_does_not_match_empty_operation()
        contain_tree = operations.make_match_one_value_operation(value_tree)
        not_contain_tree = operations.make_does_not_match_one_value_operation(value_tree)
        any_value_tree = operations.make_match_any_value_operation(value_tree)
        not_any_value_tree = operations.make_does_not_match_any_value_operation(value_tree)

        assert list(empty_tree.compile()) == ['posts.tags', 'IS EMPTY']
        assert list(not_empty_tree.compile()) == ['posts.tags', 'IS NOT EMPTY']
        assert list(contain_tree.compile()) == ['posts.tags', 'CONTAIN', 'sports']
        assert list(not_contain_tree.compile()) == ['posts.tags', 'NOT CONTAIN', 'sports']
        assert list(any_value_tree.compile()) == ['posts.tags', 'CONTAIN ANY', 'sports']
        assert list(not_any_value_tree.compile()) == ['posts.tags', 'CONTAIN NONE', 'sports']
        assert descriptors.is_badge_field.call_args_list == [call(system_field)]
        assert descriptors.is_multi_value_field.call_args_list == [call(system_field)]
        assert descriptors.get_field_alias.call_args_list == [call(system_field)]


    def test_it_should_make_single_value_range_operations_that_compile_correctly(self, fields_: Fields, descriptors: Mock | IDescriptors):
        descriptors.get_field_alias = Mock(return_value='posts.score')
        descriptors.is_badge_field = Mock(return_value=False)
        descriptors.is_multi_value_field = Mock(return_value=False)
        descriptors.is_single_value_field = Mock(return_value=True)
        min_tree = self.StubTree(compiled_output='100')
        max_tree = self.StubTree(compiled_output='1000')
        value_tree = self.StubTree(compiled_output='500')

        system_field = fields.System(name='score')
        operations = fields_.make_field_operations(system_field)
        between_tree = operations.make_between_operation(min_tree, max_tree)
        not_between_tree = operations.make_not_between_operation(min_tree, max_tree)
        less_than_tree = operations.make_less_than_operation(value_tree)
        less_equal_tree = operations.make_less_than_or_equal_operation(value_tree)
        more_than_tree = operations.make_more_than_operation(value_tree)
        more_equal_tree = operations.make_more_than_or_equal_operation(value_tree)

        assert list(between_tree.compile()) == ['posts.score', 'BETWEEN', '100', 'AND', '1000']
        assert list(not_between_tree.compile()) == ['NOT', 'posts.score', 'BETWEEN', '100', 'AND', '1000']
        assert list(less_than_tree.compile()) == ['posts.score', '<', '500']
        assert list(less_equal_tree.compile()) == ['posts.score', '<=', '500']
        assert list(more_than_tree.compile()) == ['posts.score', '>', '500']
        assert list(more_equal_tree.compile()) == ['posts.score', '>=', '500']

    def test_it_should_raise_error_for_unsupported_field_type(self, fields_: Fields, descriptors: Mock | IDescriptors):
        descriptors.is_badge_field = Mock(return_value=False)
        descriptors.is_multi_value_field = Mock(return_value=False)
        descriptors.is_single_value_field = Mock(return_value=False)

        system_field = fields.System(name='unknown')

        try:
            fields_.make_field_operations(system_field)
            assert False, 'Expected ValueError to be raised'
        except ValueError as e:
            assert str(e) == "Unsupported field: System(name='unknown'). Expected a custom, boolean, single-value, or multi-value field."

    def test_it_should_make_comprehensive_custom_field_operations(self, fields_: Fields):
        min_tree = self.StubTree(compiled_output='1')
        max_tree = self.StubTree(compiled_output='10')
        value_tree = self.StubTree(compiled_output='priority')

        custom_field = fields.Custom(name='extras', path='metadata.category')
        operations = fields_.make_field_operations(custom_field)
        badge_tree = operations.make_match_badge_operation()
        not_badge_tree = operations.make_does_not_match_badge_operation()
        empty_tree = operations.make_match_empty_operation()
        not_empty_tree = operations.make_does_not_match_empty_operation()
        one_value_tree = operations.make_match_one_value_operation(value_tree)
        not_one_value_tree = operations.make_does_not_match_one_value_operation(value_tree)
        any_value_tree = operations.make_match_any_value_operation(value_tree)
        not_any_value_tree = operations.make_does_not_match_any_value_operation(value_tree)
        between_tree = operations.make_between_operation(min_tree, max_tree)
        not_between_tree = operations.make_not_between_operation(min_tree, max_tree)
        less_than_tree = operations.make_less_than_operation(value_tree)
        less_equal_tree = operations.make_less_than_or_equal_operation(value_tree)
        more_than_tree = operations.make_more_than_operation(value_tree)
        more_equal_tree = operations.make_more_than_or_equal_operation(value_tree)

        assert list(badge_tree.compile()) == ["CUSTOM_FIELD('metadata.category')"]
        assert list(not_badge_tree.compile()) == ['NOT', "CUSTOM_FIELD('metadata.category')"]
        assert list(empty_tree.compile()) == ["CUSTOM_FIELD('metadata.category')", 'IS EMPTY']
        assert list(not_empty_tree.compile()) == ["CUSTOM_FIELD('metadata.category')", 'IS NOT EMPTY']
        assert list(one_value_tree.compile()) == ["CUSTOM_FIELD('metadata.category')", 'CONTAIN', 'priority']
        assert list(not_one_value_tree.compile()) == ["CUSTOM_FIELD('metadata.category')", 'NOT CONTAIN', 'priority']
        assert list(any_value_tree.compile()) == ["CUSTOM_FIELD('metadata.category')", 'CONTAIN ANY', 'priority']
        assert list(not_any_value_tree.compile()) == ["CUSTOM_FIELD('metadata.category')", 'CONTAIN NONE', 'priority']
        assert list(between_tree.compile()) == ["CUSTOM_FIELD('metadata.category')", 'BETWEEN', '1', 'AND', '10']
        assert list(not_between_tree.compile()) == ['NOT', "CUSTOM_FIELD('metadata.category')", 'BETWEEN', '1', 'AND', '10']
        assert list(less_than_tree.compile()) == ["CUSTOM_FIELD('metadata.category')", '<', 'priority']
        assert list(less_equal_tree.compile()) == ["CUSTOM_FIELD('metadata.category')", '<=', 'priority']
        assert list(more_than_tree.compile()) == ["CUSTOM_FIELD('metadata.category')", '>', 'priority']
        assert list(more_equal_tree.compile()) == ["CUSTOM_FIELD('metadata.category')", '>=', 'priority']

    class StubTree(sql.compiling.ITree):
        def __init__(self, compiled_output: str):
            self.compiled_output = compiled_output

        def compile(self):
            yield self.compiled_output
