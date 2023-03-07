from dataclasses import dataclass
from functools import lru_cache
from typing import Callable
from typing import Dict
from typing import Generic
from typing import Sequence
from typing import Type
from typing import TypeVar

from rmshared.content.taxonomy.core2.protocols.abc import IFilters
from rmshared.content.taxonomy.core2.protocols.abc import IOrders
from rmshared.content.taxonomy.core2.protocols.abc import ILabels
from rmshared.content.taxonomy.core2.protocols.abc import IRanges
from rmshared.content.taxonomy.core2.protocols.abc import IFields
from rmshared.content.taxonomy.core2.protocols.abc import IValues
from rmshared.content.taxonomy.core2.protocols.abc import IBuilder
from rmshared.content.taxonomy.core2.protocols.filters import Filters
from rmshared.content.taxonomy.core2.protocols.orders import Orders
from rmshared.content.taxonomy.core2.protocols.labels import Labels
from rmshared.content.taxonomy.core2.protocols.ranges import Ranges
from rmshared.content.taxonomy.core2.protocols.fields import Fields
from rmshared.content.taxonomy.core2.protocols.values import Values
from rmshared.content.taxonomy.core2.protocols.protocol import Protocol


class Builder(IBuilder):
    P = TypeVar('P')

    def __init__(self):
        self.interface_to_factory_map: Dict[IBuilder.Dependency, 'Builder.Factory'] = {
            IFilters: self.Factory(Filters, (ILabels, IRanges)),
            IOrders: self.Factory(Orders, (IFields,)),
            ILabels: self.Factory(Labels, (IFields, IValues)),
            IRanges: self.Factory(Ranges, (IFields, IValues)),
            IFields: self.Factory(Fields, ()),
            IValues: self.Factory(Values, ()),
        }

    def customize_filters(self, factory, dependencies):
        self.interface_to_factory_map[IFilters] = self.Factory(factory, dependencies)

    def customize_orders(self, factory, dependencies):
        self.interface_to_factory_map[IOrders] = self.Factory(factory, dependencies)

    def customize_labels(self, factory, dependencies):
        self.interface_to_factory_map[ILabels] = self.Factory(factory, dependencies)

    def customize_ranges(self, factory, dependencies):
        self.interface_to_factory_map[IRanges] = self.Factory(factory, dependencies)

    def customize_fields(self, factory, dependencies):
        self.interface_to_factory_map[IFields] = self.Factory(factory, dependencies)

    def customize_values(self, factory, dependencies):
        self.interface_to_factory_map[IValues] = self.Factory(factory, dependencies)

    def make_protocol(self):
        from pprint import pprint
        pprint(self.interface_to_factory_map)
        filters = self._make_protocol(IFilters)
        orders = self._make_protocol(IOrders)
        return Protocol(filters=filters, orders=orders)

    @lru_cache(maxsize=None, typed=True)
    def _make_protocol(self, interface: IBuilder.Dependency):
        factory = self.interface_to_factory_map[interface]
        dependencies = tuple(map(self._make_protocol, factory.dependencies))
        return factory.func(*dependencies)

    @dataclass(frozen=True)
    class Factory(Generic[P]):
        func: Callable[..., 'Builder.P']
        dependencies: Sequence[Type[IBuilder.Dependency]]
