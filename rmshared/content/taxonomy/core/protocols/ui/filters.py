from __future__ import annotations

from abc import ABCMeta
from abc import abstractmethod
from operator import attrgetter
from typing import Any
from typing import Collection
from typing import Generic
from typing import Mapping
from typing import Type

from rmshared.tools import dict_from_list
from rmshared.tools import ensure_map_is_complete
from rmshared.tools import parse_name_and_info

from rmshared.content.taxonomy.core import filters
from rmshared.content.taxonomy.core.protocols.abc import Filter
from rmshared.content.taxonomy.core.protocols.abc import IFilters
from rmshared.content.taxonomy.core.protocols.abc import ILabels
from rmshared.content.taxonomy.core.protocols.abc import IRanges


class Filters(IFilters[filters.Filter]):
    def __init__(self, labels: ILabels, ranges: IRanges):
        self.filter_to_delegate_map: Mapping[Type[Filter], Filters.IDelegate] = ensure_map_is_complete(filters.Filter, {
            filters.AnyLabel: self.AnyLabel(labels),
            filters.NoLabels: self.NoLabels(labels),
            filters.AnyRange: self.AnyRange(ranges),
            filters.NoRanges: self.NoRanges(ranges),
        })
        self.name_to_delegate_map: Mapping[str, Filters.IDelegate] = dict_from_list(
            source=self.filter_to_delegate_map.values(),
            key_func=attrgetter('name'),
        )

    def make_filter(self, data):
        name, info = parse_name_and_info(data)
        return self.name_to_delegate_map[name].make_filter(info)

    def jsonify_filter(self, filter_):
        delegate = self.filter_to_delegate_map[type(filter_)]
        return {delegate.name: delegate.jsonify_filter_info(filter_)}

    class IDelegate(Generic[Filter], metaclass=ABCMeta):
        @property
        @abstractmethod
        def name(self) -> str:
            ...

        @abstractmethod
        def make_filter(self, info: Collection[Any]) -> Filter:
            ...

        @abstractmethod
        def jsonify_filter_info(self, filter_: Filter) -> Collection[Any]:
            ...

    class AnyLabel(IDelegate[filters.AnyLabel]):
        def __init__(self, labels: ILabels):
            self.labels = labels

        @property
        def name(self):
            return 'any_label'

        def make_filter(self, data) -> filters.AnyLabel:
            return filters.AnyLabel(labels=tuple(map(self.labels.make_label, data)))

        def jsonify_filter_info(self, filter_: filters.AnyLabel):
            return list(map(self.labels.jsonify_label, filter_.labels))

    class NoLabels(IDelegate[filters.NoLabels]):
        def __init__(self, labels: ILabels):
            self.labels = labels

        @property
        def name(self):
            return 'no_labels'

        def make_filter(self, data) -> filters.NoLabels:
            return filters.NoLabels(labels=tuple(map(self.labels.make_label, data)))

        def jsonify_filter_info(self, filter_: filters.NoLabels):
            return list(map(self.labels.jsonify_label, filter_.labels))

    class AnyRange(IDelegate[filters.AnyRange]):
        def __init__(self, ranges: IRanges):
            self.ranges = ranges

        @property
        def name(self):
            return 'any_range'

        def make_filter(self, data) -> filters.AnyRange:
            return filters.AnyRange(ranges=tuple(map(self.ranges.make_range, data)))

        def jsonify_filter_info(self, filter_: filters.AnyRange):
            return list(map(self.ranges.jsonify_range, filter_.ranges))

    class NoRanges(IDelegate[filters.NoRanges]):
        def __init__(self, ranges: IRanges):
            self.ranges = ranges

        @property
        def name(self):
            return 'no_ranges'

        def make_filter(self, data) -> filters.NoRanges:
            return filters.NoRanges(ranges=tuple(map(self.ranges.make_range, data)))

        def jsonify_filter_info(self, filter_: filters.NoRanges):
            return list(map(self.ranges.jsonify_range, filter_.ranges))
