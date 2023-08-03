from rmshared.content.taxonomy import visitors as taxonomy_visitors
from rmshared.content.taxonomy.core import filters
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
    def make_ranges(values_: taxonomy_visitors.IValues) -> taxonomy_visitors.IRanges:
        instance = taxonomy_visitors.composites.Ranges()
        instance.add_range(ranges.Between, visitors.ranges.MapBetween(values_))
        instance.add_range(ranges.LessThan, visitors.ranges.MapLessThan(values_))
        instance.add_range(ranges.MoreThan, visitors.ranges.MapMoreThan(values_))
        return instance

    @staticmethod
    def make_values() -> taxonomy_visitors.IValues:
        instance = taxonomy_visitors.composites.Values()
        instance.add_value(str, visitors.values.AsIs())
        instance.add_value(int, visitors.values.AsIs())
        instance.add_value(float, visitors.values.AsIs())
        instance.add_value(bool, visitors.values.AsIs())
        return instance
