from mock.mock import Mock
from pytest import fixture

from rmshared.tools import ensure_map_is_complete

from rmshared.content.taxonomy.abc import Filter
from rmshared.content.taxonomy.mappers.abc import ILabels
from rmshared.content.taxonomy.mappers.abc import IRanges
from rmshared.content.taxonomy.mappers.filters import Filters


class FiltersTestCase:
    @fixture
    def filters(self, labels: ILabels, ranges: IRanges) -> Filters:
        return Filters(labels, ranges)

    @fixture
    def labels(self) -> ILabels:
        return Mock(spec=ILabels)

    @fixture
    def ranges(self) -> IRanges:
        return Mock(spec=IRanges)

    @staticmethod
    def test_filters_map_should_be_complete(filters: Filters):
        ensure_map_is_complete(Filter, filters.filter_to_factory_func_map)
