from itertools import chain
from typing import Iterator
from typing import TypeVar

from rmshared.content.taxonomy import visitors
from rmshared.content.taxonomy.core2 import filters

InLabel = TypeVar('InLabel')
OutLabel = TypeVar('OutLabel')
InRange = TypeVar('InRange')
OutRange = TypeVar('OutRange')


class ExpandAnyLabel(visitors.IFilters[filters.AnyLabel[InLabel], Iterator[filters.AnyLabel[OutLabel]]]):
    def __init__(self, labels: visitors.ILabels[InLabel, Iterator[OutLabel]]):
        self.labels = labels

    def visit_filter(self, filter_: filters.AnyLabel[InLabel]) -> Iterator[filters.AnyLabel[OutLabel]]:
        labels = chain.from_iterable(map(self.labels.visit_label, filter_.labels))
        yield filters.AnyLabel(labels=tuple(labels))


class ExpandNoLabels(visitors.IFilters[filters.NoLabels[InLabel], Iterator[filters.NoLabels[OutLabel]]]):
    def __init__(self, labels: visitors.ILabels[InLabel, Iterator[OutLabel]]):
        self.labels = labels

    def visit_filter(self, filter_: filters.NoLabels[InLabel]) -> Iterator[filters.NoLabels[OutLabel]]:
        labels = chain.from_iterable(map(self.labels.visit_label, filter_.labels))
        yield filters.NoLabels(labels=tuple(labels))


class ExpandAnyRange(visitors.IFilters[filters.AnyRange[InRange], Iterator[filters.AnyRange[OutRange]]]):
    def __init__(self, ranges: visitors.IRanges[InRange, Iterator[OutRange]]):
        self.ranges = ranges

    def visit_filter(self, filter_: filters.AnyRange[InRange]) -> Iterator[filters.AnyRange[OutRange]]:
        ranges = chain.from_iterable(map(self.ranges.visit_range, filter_.ranges))
        yield filters.AnyRange(ranges=tuple(ranges))


class ExpandNoRanges(visitors.IFilters[filters.NoRanges[InRange], Iterator[filters.NoRanges[OutRange]]]):
    def __init__(self, ranges: visitors.IRanges[InRange, Iterator[OutRange]]):
        self.ranges = ranges

    def visit_filter(self, filter_: filters.NoRanges[InRange]) -> Iterator[filters.NoRanges[OutRange]]:
        ranges = chain.from_iterable(map(self.ranges.visit_range, filter_.ranges))
        yield filters.NoRanges(ranges=tuple(ranges))
