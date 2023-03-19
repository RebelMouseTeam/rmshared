from rmshared.content.taxonomy import visitors as taxonomy_visitors
from rmshared.content.taxonomy.core import filters
from rmshared.content.taxonomy.core import labels
from rmshared.content.taxonomy.core import ranges
from rmshared.content.taxonomy.core import visitors


class Factory:
    @staticmethod
    def make_filters(labels_: taxonomy_visitors.ILabels, ranges_: taxonomy_visitors.IRanges) -> taxonomy_visitors.IFilters:
        instance = taxonomy_visitors.composites.Filters()
        instance.add_filter(filters.AnyLabel, visitors.filters.MapAnyLabel(labels_))
        instance.add_filter(filters.NoLabels, visitors.filters.MapNoLabels(labels_))
        instance.add_filter(filters.AnyRange, visitors.filters.MapAnyRange(ranges_))
        instance.add_filter(filters.NoRanges, visitors.filters.MapNoRanges(ranges_))
        return instance

    @staticmethod
    def make_orders():
        return visitors.orders.AsIs()

    @staticmethod
    def make_labels(fields_: taxonomy_visitors.IFields, values_: taxonomy_visitors.IValues) -> taxonomy_visitors.ILabels:
        instance = taxonomy_visitors.composites.Labels()
        instance.add_label(labels.Value, visitors.labels.MapValue(fields_, values_))
        instance.add_label(labels.Badge, visitors.labels.MapBadge(fields_))
        instance.add_label(labels.Empty, visitors.labels.MapEmpty(fields_))
        return instance

    @staticmethod
    def make_ranges(fields_: taxonomy_visitors.IFields, values_: taxonomy_visitors.IValues) -> taxonomy_visitors.IRanges:
        instance = taxonomy_visitors.composites.Ranges()
        instance.add_range(ranges.Between, visitors.ranges.MapBetween(fields_, values_))
        instance.add_range(ranges.LessThan, visitors.ranges.MapLessThan(fields_, values_))
        instance.add_range(ranges.MoreThan, visitors.ranges.MapMoreThan(fields_, values_))
        return instance

    @staticmethod
    def make_values() -> taxonomy_visitors.IValues:
        instance = taxonomy_visitors.composites.Values()
        instance.add_value(str, visitors.values.AsIs())
        instance.add_value(int, visitors.values.AsIs())
        instance.add_value(float, visitors.values.AsIs())
        instance.add_value(bool, visitors.values.AsIs())
        return instance

    @staticmethod
    def make_fields():
        return visitors.fields.AsIs()
