from unittest.mock import Mock
from unittest.mock import call
from pytest import fixture

from rmshared.content.taxonomy.core import fields
from rmshared.content.taxonomy.core import filters
from rmshared.content.taxonomy.core import labels
from rmshared.content.taxonomy.core import ranges
from rmshared.content.taxonomy.core import traversal
from rmshared.content.taxonomy.core.sql.compiling.abc import IDescriptors
from rmshared.content.taxonomy.core.sql.compiling.fields import Fields
from rmshared.content.taxonomy.core.sql.compiling.values import Values
from rmshared.content.taxonomy.core.sql.compiling.labels import Labels
from rmshared.content.taxonomy.core.sql.compiling.ranges import Ranges
from rmshared.content.taxonomy.core.sql.compiling.filters import Filters


class TestFilters:
    @fixture
    def filters_(self, labels_: Labels, ranges_: Ranges) -> Filters:
        return Filters(labels_, ranges_)

    @fixture
    def labels_(self, fields_: Fields, values: Values) -> Labels:
        traversal_ = traversal.Factory.make_instance().make_labels()
        return Labels(fields_, values, traversal_)

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

    def test_it_should_compile_any_label_filter(self, filters_: Filters, descriptors: Mock | IDescriptors):
        descriptors.get_field_alias = Mock(side_effect=lambda field: f'posts.{field.name}')
        descriptors.is_badge_field = Mock(side_effect=lambda field: field.name == 'is_featured')
        descriptors.is_single_value_field = Mock(side_effect=lambda field: field.name == 'status')
        descriptors.is_multi_value_field = Mock(side_effect=lambda field: False)

        status_field = fields.System(name='status')
        featured_field = fields.System(name='is_featured')
        status_label = labels.Value(field=status_field, value='published')
        featured_label = labels.Badge(field=featured_field)
        filter_ = filters.AnyLabel(labels=[status_label, featured_label])
        tree = filters_.make_tree_from_filter(filter_)
        compiled = list(tree.compile())

        assert compiled == ['(', 'posts.status', 'IS', "'published'", 'OR', 'posts.is_featured', ')']
        assert descriptors.get_field_alias.call_args_list == [call(status_field), call(featured_field)]
        assert descriptors.is_badge_field.call_args_list == [call(status_field), call(featured_field)]
        assert descriptors.is_single_value_field.call_args_list == [call(status_field)]

    def test_it_should_compile_no_labels_filter(self, filters_: Filters, descriptors: Mock | IDescriptors):
        descriptors.get_field_alias = Mock(side_effect=lambda field: f'posts.{field.name}')
        descriptors.is_badge_field = Mock(side_effect=lambda field: field.name == 'is_featured')
        descriptors.is_single_value_field = Mock(side_effect=lambda field: field.name == 'status')
        descriptors.is_multi_value_field = Mock(side_effect=lambda field: False)

        status_field = fields.System(name='status')
        featured_field = fields.System(name='is_featured')
        status_label = labels.Value(field=status_field, value='draft')
        featured_label = labels.Badge(field=featured_field)
        filter_ = filters.NoLabels(labels=[status_label, featured_label])
        tree = filters_.make_tree_from_filter(filter_)
        compiled = list(tree.compile())

        assert compiled == ['posts.status', 'IS NOT', "'draft'", ' ', 'AND', 'NOT', 'posts.is_featured']
        assert descriptors.get_field_alias.call_args_list == [call(status_field), call(featured_field)]
        assert descriptors.is_badge_field.call_args_list == [call(status_field), call(featured_field)]
        assert descriptors.is_single_value_field.call_args_list == [call(status_field)]

    def test_it_should_compile_any_range_filter(self, filters_: Filters, descriptors: Mock | IDescriptors):
        descriptors.get_field_alias = Mock(side_effect=lambda field: f'posts.{field.name}')
        descriptors.is_badge_field = Mock(return_value=False)
        descriptors.is_single_value_field = Mock(return_value=True)
        descriptors.is_multi_value_field = Mock(return_value=False)

        created_field = fields.System(name='created_at')
        score_field = fields.System(name='score')
        date_range = ranges.Between(field=created_field, min_value='2024-01-01', max_value='2024-12-31')
        score_range = ranges.MoreThan(field=score_field, value=500)
        filter_ = filters.AnyRange(ranges=[date_range, score_range])
        tree = filters_.make_tree_from_filter(filter_)
        compiled = list(tree.compile())

        assert compiled == ['(', 'posts.created_at', 'BETWEEN', "'2024-01-01'", 'AND', "'2024-12-31'", 'OR', 'posts.score', '>', '500', ')']
        assert descriptors.get_field_alias.call_args_list == [call(created_field), call(score_field)]
        assert descriptors.is_badge_field.call_args_list == [call(created_field), call(score_field)]
        assert descriptors.is_single_value_field.call_args_list == [call(created_field), call(score_field)]

    def test_it_should_compile_no_ranges_filter(self, filters_: Filters, descriptors: Mock | IDescriptors):
        descriptors.get_field_alias = Mock(side_effect=lambda field: f'posts.{field.name}')
        descriptors.is_badge_field = Mock(return_value=False)
        descriptors.is_single_value_field = Mock(return_value=True)
        descriptors.is_multi_value_field = Mock(return_value=False)

        view_field = fields.System(name='view_count')
        engagement_field = fields.System(name='engagement_score')
        view_range = ranges.LessThan(field=view_field, value=100)
        engagement_range = ranges.LessThan(field=engagement_field, value=10)
        filter_ = filters.NoRanges(ranges=[view_range, engagement_range])
        tree = filters_.make_tree_from_filter(filter_)
        compiled = list(tree.compile())

        assert compiled == ['posts.view_count', '>=', '100', ' ', 'AND', 'posts.engagement_score', '>=', '10']
        assert descriptors.get_field_alias.call_args_list == [call(view_field), call(engagement_field)]
        assert descriptors.is_badge_field.call_args_list == [call(view_field), call(engagement_field)]
        assert descriptors.is_single_value_field.call_args_list == [call(view_field), call(engagement_field)]
