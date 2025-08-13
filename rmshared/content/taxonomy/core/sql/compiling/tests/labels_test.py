from unittest.mock import Mock
from unittest.mock import call
from pytest import fixture

from rmshared.content.taxonomy.core import fields
from rmshared.content.taxonomy.core import labels
from rmshared.content.taxonomy.core import traversal
from rmshared.content.taxonomy.core.sql.compiling.abc import IDescriptors
from rmshared.content.taxonomy.core.sql.compiling.fields import Fields
from rmshared.content.taxonomy.core.sql.compiling.values import Values
from rmshared.content.taxonomy.core.sql.compiling.labels import Labels


class TestLabels:
    @fixture
    def labels_(self, fields_: Fields, values: Values) -> Labels:
        traversal_ = traversal.Factory.make_instance().make_labels()
        return Labels(fields_, values, traversal_)

    @fixture
    def fields_(self, descriptors: IDescriptors) -> Fields:
        return Fields(descriptors)

    @fixture
    def values(self) -> Values:
        return Values()

    @fixture
    def descriptors(self) -> Mock | IDescriptors:
        return Mock(spec=IDescriptors)

    def test_it_should_compile_badge_label(self, labels_: Labels, descriptors: Mock | IDescriptors):
        descriptors.get_field_alias = Mock(return_value='posts.is_featured')
        descriptors.is_badge_field = Mock(return_value=True)
        descriptors.is_multi_value_field = Mock(return_value=False)
        descriptors.is_single_value_field = Mock(return_value=False)

        field = fields.System(name='is_featured')
        label = labels.Badge(field=field)
        tree = labels_.make_tree_from_labels(labels_=[label], matcher=labels_.Match())
        compiled = list(tree.compile())
        tree_not = labels_.make_tree_from_labels(labels_=[label], matcher=labels_.MatchNot())
        compiled_not = list(tree_not.compile())

        assert compiled == ['posts.is_featured']
        assert compiled_not == ['NOT', 'posts.is_featured']
        assert descriptors.get_field_alias.call_args_list == [call(field), call(field)]

    def test_it_should_compile_empty_label_on_multi_value_field(self, labels_: Labels, descriptors: Mock | IDescriptors):
        descriptors.get_field_alias = Mock(return_value='posts.sections')
        descriptors.is_badge_field = Mock(return_value=False)
        descriptors.is_multi_value_field = Mock(return_value=True)
        descriptors.is_single_value_field = Mock(return_value=False)

        field = fields.System(name='sections')
        label = labels.Empty(field=field)
        tree = labels_.make_tree_from_labels(labels_=[label], matcher=labels_.Match())
        compiled = list(tree.compile())
        tree_not = labels_.make_tree_from_labels(labels_=[label], matcher=labels_.MatchNot())
        compiled_not = list(tree_not.compile())

        assert compiled == ['posts.sections', 'IS EMPTY']
        assert compiled_not == ['posts.sections', 'IS NOT EMPTY']
        assert descriptors.get_field_alias.call_args_list == [call(field), call(field)]

    def test_it_should_compile_empty_label_on_single_value_field(self, labels_: Labels, descriptors: Mock | IDescriptors):
        descriptors.get_field_alias = Mock(return_value='posts.description')
        descriptors.is_badge_field = Mock(return_value=False)
        descriptors.is_multi_value_field = Mock(return_value=False)
        descriptors.is_single_value_field = Mock(return_value=True)

        field = fields.System(name='description')
        label = labels.Empty(field=field)
        tree = labels_.make_tree_from_labels(labels_=[label], matcher=labels_.Match())
        compiled = list(tree.compile())
        tree_not = labels_.make_tree_from_labels(labels_=[label], matcher=labels_.MatchNot())
        compiled_not = list(tree_not.compile())

        assert compiled == ['posts.description', 'IS NULL']
        assert compiled_not == ['posts.description', 'IS NOT NULL']
        assert descriptors.get_field_alias.call_args_list == [call(field), call(field)]

    def test_it_should_compile_value_label_on_single_value_field(self, labels_: Labels, descriptors: Mock | IDescriptors):
        descriptors.get_field_alias = Mock(return_value='posts.status')
        descriptors.is_badge_field = Mock(return_value=False)
        descriptors.is_multi_value_field = Mock(return_value=False)
        descriptors.is_single_value_field = Mock(return_value=True)

        field = fields.System(name='status')
        label = labels.Value(field=field, value='published')
        tree = labels_.make_tree_from_labels(labels_=[label], matcher=labels_.Match())
        compiled = list(tree.compile())
        tree_not = labels_.make_tree_from_labels(labels_=[label], matcher=labels_.MatchNot())
        compiled_not = list(tree_not.compile())

        assert compiled == ['posts.status', 'IS', "'published'"]
        assert compiled_not == ['posts.status', 'IS NOT', "'published'"]
        assert descriptors.get_field_alias.call_args_list == [call(field), call(field)]

    def test_it_should_compile_value_label_on_multi_value_field(self, labels_: Labels, descriptors: Mock | IDescriptors):
        descriptors.get_field_alias = Mock(return_value='posts.tags')
        descriptors.is_badge_field = Mock(return_value=False)
        descriptors.is_multi_value_field = Mock(return_value=True)
        descriptors.is_single_value_field = Mock(return_value=False)

        field = fields.System(name='tags')
        label = labels.Value(field=field, value='tech')
        tree = labels_.make_tree_from_labels(labels_=[label], matcher=labels_.Match())
        compiled = list(tree.compile())
        tree_not = labels_.make_tree_from_labels(labels_=[label], matcher=labels_.MatchNot())
        compiled_not = list(tree_not.compile())

        assert compiled == ['posts.tags', 'CONTAIN', "'tech'"]
        assert compiled_not == ['posts.tags', 'NOT CONTAIN', "'tech'"]
        assert descriptors.get_field_alias.call_args_list == [call(field), call(field)]

    def test_it_should_compile_multiple_label_types(self, labels_: Labels, descriptors: Mock | IDescriptors):
        descriptors.get_field_alias = Mock(side_effect=lambda field: {
            'status': 'posts.status',
            'is_featured': 'posts.is_featured', 
            'sections': 'posts.sections'
        }[field.name])
        descriptors.is_badge_field = Mock(side_effect=lambda field: field.name == 'is_featured')
        descriptors.is_single_value_field = Mock(side_effect=lambda field: field.name == 'status')
        descriptors.is_multi_value_field = Mock(side_effect=lambda field: field.name == 'sections')

        status_field = fields.System(name='status')
        featured_field = fields.System(name='is_featured')
        sections_field = fields.System(name='sections')
        value_label = labels.Value(field=status_field, value='published')
        badge_label = labels.Badge(field=featured_field)
        empty_label = labels.Empty(field=sections_field)
        tree = labels_.make_tree_from_labels(labels_=[value_label, badge_label, empty_label], matcher=labels_.Match())
        compiled = list(tree.compile())

        assert compiled == ['(', 'posts.status', 'IS', "'published'", 'OR', 'posts.is_featured', 'OR', 'posts.sections', 'IS EMPTY', ')']
        assert descriptors.get_field_alias.call_args_list == [call(status_field), call(featured_field), call(sections_field)]
