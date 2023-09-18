from typing import Mapping
from typing import Type
from typing import TypeVar

from rmshared.tools import invert_dict

from rmshared.content.taxonomy.variables import arguments
from rmshared.content.taxonomy.variables.abc import Reference
from rmshared.content.taxonomy.variables.protocols.abc import IVariables

Argument = TypeVar('Argument', bound=arguments.Argument)


class Variables(IVariables):
    def __init__(self):
        self.argument_to_argument_name_map: Mapping[Type[Argument], str] = {
            arguments.Value: '@value',
            arguments.Empty: '@empty',
            arguments.Any: '@any',
        }
        self.argument_name_to_argument_map: Mapping[str, Type[Argument]] = invert_dict(self.argument_to_argument_name_map)

    def make_argument(self, data):
        return self.argument_name_to_argument_map[data]

    def jsonify_argument(self, argument):
        return self.argument_to_argument_name_map[argument]

    def make_reference(self, data):
        return Reference(alias=str(data['alias']))

    def jsonify_reference(self, reference):
        return {'alias': reference.alias}

    def make_variable(self, data):
        reference = self.make_reference(data['ref'])
        return reference, int(data['index'])

    def jsonify_variable(self, reference, index):
        return {'ref': self.jsonify_reference(reference), 'index': index}
