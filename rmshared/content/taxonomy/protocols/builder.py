from dataclasses import dataclass
from functools import lru_cache
from typing import Callable
from typing import Generic
from typing import Mapping
from typing import Sequence
from typing import Type
from typing import TypeVar

from rmshared.content.taxonomy.protocols.abc import IFilters
from rmshared.content.taxonomy.protocols.abc import IOrders
from rmshared.content.taxonomy.protocols.abc import ILabels
from rmshared.content.taxonomy.protocols.abc import IRanges
from rmshared.content.taxonomy.protocols.abc import IFields
from rmshared.content.taxonomy.protocols.abc import IValues
from rmshared.content.taxonomy.protocols.abc import IBuilder
from rmshared.content.taxonomy.protocols.protocol import Protocol


class Builder(IBuilder):
    P = TypeVar('P')

    def __init__(self, interface_to_factory_map: Mapping[IBuilder.Dependency, 'Builder.Factory'] = None):
        self.interface_to_factory_map = dict(interface_to_factory_map or dict())

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
        filters = self._make_protocol(IFilters)
        orders = self._make_protocol(IOrders)
        fields = self._make_protocol(IFields)
        return Protocol(filters=filters, orders=orders, fields=fields)

    @lru_cache(maxsize=16, typed=True)
    def _make_protocol(self, interface: IBuilder.Dependency):
        factory = self.interface_to_factory_map[interface]
        dependencies = tuple(map(self._make_protocol, factory.dependencies))
        return factory.func(*dependencies)

    @dataclass(frozen=True)
    class Factory(Generic[P]):
        func: Callable[..., 'Builder.P']
        dependencies: Sequence[Type[IBuilder.Dependency]]
