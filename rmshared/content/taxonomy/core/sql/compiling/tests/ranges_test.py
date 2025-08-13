from unittest.mock import Mock
from unittest.mock import call
from pytest import fixture

from rmshared.content.taxonomy.core import fields
from rmshared.content.taxonomy.core import ranges
from rmshared.content.taxonomy.core import traversal
from rmshared.content.taxonomy.core.sql.compiling.abc import IDescriptors
from rmshared.content.taxonomy.core.sql.compiling.fields import Fields
from rmshared.content.taxonomy.core.sql.compiling.values import Values
from rmshared.content.taxonomy.core.sql.compiling.ranges import Ranges


class TestRanges:
    @fixture
    def ranges_(self, fields_: Fields, values: Values) -> Ranges:
        traversal_ = traversal.Factory.make_instance().make_ranges()
        return Ranges(fields_, values, traversal_)

    @fixture
    def fields_(self, descriptors: IDescriptors) -> Fields:
        return Fields(descriptors)

    @fixture
    def values(self) -> Values:
        return Values()

    @fixture
    def descriptors(self) -> Mock | IDescriptors:
        return Mock(spec=IDescriptors)

    def test_it_should_compile_between_range(self, ranges_: Ranges, descriptors: Mock | IDescriptors):
        descriptors.get_field_alias = Mock(return_value='posts.created_at')
        descriptors.is_badge_field = Mock(return_value=False)
        descriptors.is_multi_value_field = Mock(return_value=False)
        descriptors.is_single_value_field = Mock(return_value=True)

        field = fields.System(name='created_at')
        range_ = ranges.Between(field=field, min_value='2024-01-01', max_value='2024-12-31')
        tree = ranges_.make_tree_from_ranges(ranges_=[range_], matcher=ranges_.Match())
        compiled = list(tree.compile())
        tree_not = ranges_.make_tree_from_ranges(ranges_=[range_], matcher=ranges_.MatchNot())
        compiled_not = list(tree_not.compile())

        assert compiled == ['posts.created_at', 'BETWEEN', "'2024-01-01'", 'AND', "'2024-12-31'"]
        assert compiled_not == ['NOT', 'posts.created_at', 'BETWEEN', "'2024-01-01'", 'AND', "'2024-12-31'"]
        assert descriptors.get_field_alias.call_args_list == [call(field), call(field)]

    def test_it_should_compile_less_than_range(self, ranges_: Ranges, descriptors: Mock | IDescriptors):
        descriptors.get_field_alias = Mock(return_value='posts.view_count')
        descriptors.is_badge_field = Mock(return_value=False)
        descriptors.is_multi_value_field = Mock(return_value=False)
        descriptors.is_single_value_field = Mock(return_value=True)

        field = fields.System(name='view_count')
        range_ = ranges.LessThan(field=field, value=1000)
        tree = ranges_.make_tree_from_ranges(ranges_=[range_], matcher=ranges_.Match())
        compiled = list(tree.compile())
        tree_not = ranges_.make_tree_from_ranges(ranges_=[range_], matcher=ranges_.MatchNot())
        compiled_not = list(tree_not.compile())

        assert compiled == ['posts.view_count', '<', '1000']
        assert compiled_not == ['posts.view_count', '>=', '1000']
        assert descriptors.get_field_alias.call_args_list == [call(field), call(field)]

    def test_it_should_compile_more_than_range(self, ranges_: Ranges, descriptors: Mock | IDescriptors):
        descriptors.get_field_alias = Mock(return_value='posts.popularity_score')
        descriptors.is_badge_field = Mock(return_value=False)
        descriptors.is_multi_value_field = Mock(return_value=False)
        descriptors.is_single_value_field = Mock(return_value=True)

        field = fields.System(name='popularity_score')
        range_ = ranges.MoreThan(field=field, value=500)
        tree = ranges_.make_tree_from_ranges(ranges_=[range_], matcher=ranges_.Match())
        compiled = list(tree.compile())
        tree_not = ranges_.make_tree_from_ranges(ranges_=[range_], matcher=ranges_.MatchNot())
        compiled_not = list(tree_not.compile())

        assert compiled == ['posts.popularity_score', '>', '500']
        assert compiled_not == ['posts.popularity_score', '<=', '500']
        assert descriptors.get_field_alias.call_args_list == [call(field), call(field)]

    def test_it_should_compile_multiple_range_types(self, ranges_: Ranges, descriptors: Mock | IDescriptors):
        descriptors.get_field_alias = Mock(side_effect=['posts.created_at', 'posts.view_count', 'posts.popularity_score'])
        descriptors.is_badge_field = Mock(return_value=False)
        descriptors.is_multi_value_field = Mock(return_value=False)
        descriptors.is_single_value_field = Mock(return_value=True)

        created_field = fields.System(name='created_at')
        view_field = fields.System(name='view_count')
        score_field = fields.System(name='popularity_score')
        between_range = ranges.Between(field=created_field, min_value='2024-01-01', max_value='2024-12-31')
        less_than_range = ranges.LessThan(field=view_field, value=1000)
        more_than_range = ranges.MoreThan(field=score_field, value=500)
        tree = ranges_.make_tree_from_ranges(ranges_=[between_range, less_than_range, more_than_range], matcher=ranges_.Match())
        compiled = list(tree.compile())

        assert compiled == [
            '(',
                      'posts.created_at', 'BETWEEN', "'2024-01-01'", 'AND', "'2024-12-31'",
                'OR', 'posts.view_count', '<', '1000',
                'OR', 'posts.popularity_score', '>', '500',
            ')'
        ]
        assert descriptors.get_field_alias.call_args_list == [call(created_field), call(view_field), call(score_field)]
