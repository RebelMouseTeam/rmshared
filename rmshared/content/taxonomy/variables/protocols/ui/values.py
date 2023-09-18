from abc import ABCMeta
from abc import abstractmethod
from collections import OrderedDict
from typing import Any
from typing import Generic
from typing import Type
from typing import TypeVar

from rmshared.tools import ensure_map_is_complete

from rmshared.content.taxonomy import core
from rmshared.content.taxonomy.variables import values
from rmshared.content.taxonomy.variables.protocols.abc import IVariables

Value = TypeVar('Value', bound=values.Value)


class Values(core.protocols.IValues[Value]):
    def __init__(self, variables: IVariables, delegate: core.protocols.IValues):
        self.value_to_delegate_map: OrderedDict[Type[Value], 'Values.IDelegate[Value]'] = ensure_map_is_complete(values.Value, OrderedDict([
            (values.Variable, self.Variable(variables)),
            (values.Constant, self.Constant(delegate)),
        ]))

    def make_value(self, data):
        for delegate in self.value_to_delegate_map.values():
            try:
                return delegate.make_value(data)
            except ValueError:
                pass
        else:
            raise ValueError(f'Could not make value from {data}')

    def jsonify_value(self, value):
        return self.value_to_delegate_map[type(value)].jsonify_value(value)

    class IDelegate(Generic[Value], metaclass=ABCMeta):
        @abstractmethod
        def make_value(self, data: Any) -> Value:
            """
            :raise: ValueError
            """

        @abstractmethod
        def jsonify_value(self, value: Value) -> Any:
            pass

    class Variable(IDelegate[values.Variable]):
        def __init__(self, variables: IVariables):
            self.variables = variables

        def make_value(self, data):
            reference, index = self.variables.make_variable(data)
            return values.Variable(reference, index)

        def jsonify_value(self, value: values.Variable):
            return self.variables.jsonify_variable(value.ref, value.index)

    class Constant(core.protocols.IValues[values.Constant]):
        def __init__(self, delegate: core.protocols.IValues):
            self.delegate = delegate

        def make_value(self, data):
            return values.Constant(value=self.delegate.make_value(data))

        def jsonify_value(self, value: values.Constant):
            return self.delegate.jsonify_value(value.value)
