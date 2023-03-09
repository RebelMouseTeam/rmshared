from mock.mock import Mock
from mock.mock import call

from rmshared.content.taxonomy.protocols.abc import IFields
from rmshared.content.taxonomy.protocols.abc import IFilters
from rmshared.content.taxonomy.protocols.abc import ILabels
from rmshared.content.taxonomy.protocols.abc import IOrders
from rmshared.content.taxonomy.protocols.abc import IRanges
from rmshared.content.taxonomy.protocols.abc import IProtocol
from rmshared.content.taxonomy.protocols.abc import IValues
from rmshared.content.taxonomy.protocols.builder import Builder


class TestServerBuilder:
    NOW = 1440000000

    def test_it_should_make_protocol(self):
        filters = Mock(spec=IFilters)
        filters_factory = Mock(return_value=filters)
        orders = Mock(spec=IOrders)
        orders_factory = Mock(return_value=orders)
        labels = Mock(spec=ILabels)
        labels_factory = Mock(return_value=labels)
        ranges = Mock(spec=IRanges)
        ranges_factory = Mock(return_value=ranges)
        fields = Mock(spec=IFields)
        fields_factory = Mock(return_value=fields)
        values = Mock(spec=IValues)
        values_factory = Mock(return_value=values)

        builder = Builder(interface_to_factory_map={
            IFields: Builder.Factory(fields_factory, ()),
            IValues: Builder.Factory(values_factory, ()),
            IOrders: Builder.Factory(orders_factory, ()),
        })
        builder.customize_filters(filters_factory, dependencies=(ILabels, IRanges))
        builder.customize_orders(orders_factory, dependencies=(IFields,))
        builder.customize_labels(labels_factory, dependencies=(IFields, IValues))
        builder.customize_ranges(ranges_factory, dependencies=(IFields, IValues))

        protocol = builder.make_protocol()

        assert isinstance(protocol, IProtocol)
        assert filters_factory.call_args_list == [call(labels, ranges)]
        assert orders_factory.call_args_list == [call(fields)]
        assert labels_factory.call_args_list == [call(fields, values)]
        assert ranges_factory.call_args_list == [call(fields, values)]
        assert fields_factory.call_args_list == [call()]
        assert values_factory.call_args_list == [call()]
