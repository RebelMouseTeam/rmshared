import re

from rmshared.sql import compiling

from rmshared.content.taxonomy.variables.abc import Reference
from rmshared.content.taxonomy.variables.sql.compiling.abc import IVariables


class Variables(IVariables):
    REFERENCE_BY_INDEX_REGEXP = re.compile(r'^\$\d+$')

    def make_tree_from_reference(self, reference: Reference):
        if match := self.REFERENCE_BY_INDEX_REGEXP.match(reference.alias):
            return compiling.terminals.CName(name=f'@@{match.group(1)}')
        else:
            return compiling.terminals.CName(name=f'@{reference.alias}')
