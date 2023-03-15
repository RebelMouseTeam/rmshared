from typing import TypeVar

from rmshared.content.taxonomy import protocols as taxonomy_protocols

from rmshared.content.taxonomy.core import filters
from rmshared.content.taxonomy.core import orders
from rmshared.content.taxonomy.core import labels
from rmshared.content.taxonomy.core import ranges
from rmshared.content.taxonomy.core import fields
from rmshared.content.taxonomy.core import protocols

Scalar = TypeVar('Scalar', str, int, float)


class Factory:
    def make_protocol(self) -> taxonomy_protocols.IProtocol[filters.Filter, orders.Order, labels.Label, ranges.Range, fields.Field, Scalar]:
        builder = taxonomy_protocols.Builder()
        builder.customize_filters(self.make_filters, dependencies=(taxonomy_protocols.ILabels, taxonomy_protocols.IRanges))
        builder.customize_orders(self.make_orders, dependencies=(taxonomy_protocols.IFields,))
        builder.customize_labels(self.make_labels, dependencies=(taxonomy_protocols.IFields, taxonomy_protocols.IValues))
        builder.customize_ranges(self.make_ranges, dependencies=(taxonomy_protocols.IFields, taxonomy_protocols.IValues))
        builder.customize_fields(self.make_fields, dependencies=())
        builder.customize_values(self.make_values, dependencies=())
        return builder.make_protocol()

    @staticmethod
    def make_filters(labels_: taxonomy_protocols.ILabels, ranges_: taxonomy_protocols.IRanges) -> taxonomy_protocols.IFilters[filters.Filter]:
        protocol = taxonomy_protocols.Filters()
        protocol.add_filter(filters.AnyLabel, protocols.filters.AnyLabel(labels_))
        protocol.add_filter(filters.NoLabels, protocols.filters.NoLabels(labels_))
        protocol.add_filter(filters.AnyRange, protocols.filters.AnyRange(ranges_))
        protocol.add_filter(filters.NoRanges, protocols.filters.NoRanges(ranges_))
        return protocol

    @staticmethod
    def make_orders(fields_: taxonomy_protocols.IFields) -> taxonomy_protocols.IOrders:
        protocol = taxonomy_protocols.Orders()
        protocol.add_order(orders.Value, protocols.orders.Value(fields_))
        return protocol

    @staticmethod
    def make_labels(fields_: taxonomy_protocols.IFields, values_: taxonomy_protocols.IValues) -> taxonomy_protocols.ILabels[labels.Label]:
        protocol = taxonomy_protocols.Labels()
        protocol.add_label(labels.Value, protocols.labels.Value(fields_, values_))
        protocol.add_label(labels.Badge, protocols.labels.Badge(fields_))
        protocol.add_label(labels.Empty, protocols.labels.Empty(fields_))
        return protocol

    @staticmethod
    def make_ranges(fields_: taxonomy_protocols.IFields, values_: taxonomy_protocols.IValues) -> taxonomy_protocols.IRanges[ranges.Range]:
        protocol = taxonomy_protocols.Ranges()
        protocol.add_range(ranges.Between, protocols.ranges.Between(fields_, values_))
        protocol.add_range(ranges.LessThan, protocols.ranges.LessThan(fields_, values_))
        protocol.add_range(ranges.MoreThan, protocols.ranges.MoreThan(fields_, values_))
        return protocol

    @staticmethod
    def make_fields() -> taxonomy_protocols.IFields[fields.Field]:
        protocol = taxonomy_protocols.Fields()
        protocol.add_field(fields.System, protocols.fields.System())
        protocol.add_field(fields.Custom, protocols.fields.Custom())
        return protocol

    @staticmethod
    def make_values() -> taxonomy_protocols.IValues:
        protocol = taxonomy_protocols.Values()
        protocol.add_value(protocols.values.Scalar(value_types=frozenset({str, int, float})))
        return protocol