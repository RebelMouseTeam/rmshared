from abc import ABCMeta
from abc import abstractmethod
from typing import Generic
from typing import Sequence
from typing import TypeVar

from rmshared.content.taxonomy.abc import Label
from rmshared.content.taxonomy.abc import Range
from rmshared.content.taxonomy.abc import Filter
from rmshared.content.taxonomy.variables.abc import Variable

ConcreteValues = TypeVar('ConcreteValues', bound=Variable)


class ILabelsProducer(Generic[ConcreteValues], metaclass=ABCMeta):
    @abstractmethod
    def produce_labels(self, values: ConcreteValues) -> Sequence[Label]:
        pass


class IRangesProducer(Generic[ConcreteValues], metaclass=ABCMeta):
    @abstractmethod
    def produce_ranges(self, values: ConcreteValues) -> Sequence[Range]:
        pass


class IFiltersProducer(Generic[ConcreteValues], metaclass=ABCMeta):
    @abstractmethod
    def produce_filters(self, values: ConcreteValues) -> Sequence[Filter]:
        pass
