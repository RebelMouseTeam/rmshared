from rmshared.content.taxonomy import visitors as taxonomy_visitors
from rmshared.content.taxonomy.core import filters
from rmshared.content.taxonomy.core import labels
from rmshared.content.taxonomy.core import ranges
from rmshared.content.taxonomy.core import visitors


class Factory:
    @staticmethod
    def make_filters(labels_: taxonomy_visitors.ILabels, ranges_: taxonomy_visitors.IRanges) -> taxonomy_visitors.IFilters:
        instance = taxonomy_visitors.composites.Filters()
        instance.add_filter(filters.AnyLabel, visitors.filters.ExpandAnyLabel(labels_))
        instance.add_filter(filters.NoLabels, visitors.filters.ExpandNoLabels(labels_))
        instance.add_filter(filters.AnyRange, visitors.filters.ExpandAnyRange(ranges_))
        instance.add_filter(filters.NoRanges, visitors.filters.ExpandNoRanges(ranges_))
        return instance

    @staticmethod
    def make_labels(values_: taxonomy_visitors.IValues) -> taxonomy_visitors.ILabels:
        instance = taxonomy_visitors.composites.Labels()
        instance.add_label(labels.Value, visitors.labels.ExpandValue(values_))
        instance.add_label(labels.Badge, visitors.labels.ExpandAsIs())
        instance.add_label(labels.Empty, visitors.labels.ExpandAsIs())
        return instance

    @staticmethod
    def make_ranges(values_: taxonomy_visitors.IValues) -> taxonomy_visitors.IRanges:
        instance = taxonomy_visitors.composites.Ranges()
        instance.add_range(ranges.Between, visitors.ranges.ExpandBetween(values_))
        instance.add_range(ranges.LessThan, visitors.ranges.ExpandLessThan(values_))
        instance.add_range(ranges.MoreThan, visitors.ranges.ExpandMoreThan(values_))
        return instance

    @staticmethod
    def make_values() -> taxonomy_visitors.IValues:
        instance = taxonomy_visitors.composites.Values()
        instance.add_value(str, visitors.values.AsIs())
        instance.add_value(int, visitors.values.AsIs())
        instance.add_value(float, visitors.values.AsIs())
        instance.add_value(bool, visitors.values.AsIs())
        return instance
