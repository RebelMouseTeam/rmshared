from unittest.mock import Mock

from pytest import fixture

from rmshared.content.taxonomy.core.fakes import Fakes
from rmshared.content.taxonomy.core.traversal.visitors.abc import IFields
from rmshared.content.taxonomy.core.traversal.visitors.fields import Fields


class TestFields:
    @fixture
    def fields(self) -> IFields | Mock:
        return Mock(spec=IFields)

    @fixture
    def non_visitor(self) -> Mock:
        return Mock()

    @fixture
    def fakes(self):
        return Fakes()

    def test_it_should_delegate_field_visit(self, fakes: Fakes, fields: IFields | Mock):
        fields.visit_field = Mock()
        visitor = Fields(delegate=fields)

        field = fakes.make_field()
        visitor.visit_field(field)

        fields.visit_field.assert_called_once_with(field)

    def test_it_should_not_delegate_field_visit(self, fakes: Fakes, non_visitor: Mock):
        visitor = Fields(delegate=non_visitor)

        field = fakes.make_field()
        visitor.visit_field(field)

        assert not hasattr(non_visitor, 'visit_field') or not non_visitor.visit_field.called

    def test_it_should_not_fail_none_delegate(self, fakes: Fakes):
        visitor = Fields(delegate=None)
        visitor.visit_field(field=fakes.make_field())
