import re

from typing import Mapping
from typing import Type
from typing import TypeVar

from rmshared.tools import invert_dict

from rmshared.content.taxonomy.variables import arguments
from rmshared.content.taxonomy.variables.abc import Reference
from rmshared.content.taxonomy.variables.protocols.abc import IVariables

Argument = TypeVar('Argument', bound=arguments.Argument)


class Variables(IVariables):
    ALIAS_REGEX = re.compile(r'^\$(?P<alias>\$\d+|\w+)$')
    VALUE_REGEX = re.compile(r'^\$(?P<alias>\$\d+|\w+)(?:\[(?P<index>\d+)])?$')

    def __init__(self):
        self.argument_to_argument_name_map: Mapping[Type[Argument], str] = {
            arguments.Value: '$each',
            arguments.Empty: '$none',
            arguments.Any: '$any',
        }
        self.argument_name_to_argument_map: Mapping[str, Type[Argument]] = invert_dict(self.argument_to_argument_name_map)

    def make_argument(self, data):
        return self.argument_name_to_argument_map[data]

    def jsonify_argument(self, argument):
        return self.argument_to_argument_name_map[argument]

    def make_reference(self, data):
        if match := self.ALIAS_REGEX.match(str(data)):
            return Reference(alias=match.group('alias'))
        else:
            raise ValueError(['invalid_reference', data])

    def jsonify_reference(self, reference):
        return f'${reference.alias}'

    def make_variable(self, data):
        if match := self.VALUE_REGEX.match(str(data)):
            reference = Reference(alias=match.group('alias'))
            index = int(match.group('index'))
            return reference, index
        else:
            raise ValueError(['invalid_variable', data])

    def jsonify_variable(self, reference, index):
        return f'${reference.alias}[{index}]'
