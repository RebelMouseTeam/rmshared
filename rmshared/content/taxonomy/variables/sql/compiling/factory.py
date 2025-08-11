from rmshared.content.taxonomy import core

from rmshared.content.taxonomy.variables.sql.compiling.abc import IComposite
from rmshared.content.taxonomy.variables.sql.compiling.assembler import Assembler
from rmshared.content.taxonomy.variables.sql.compiling.composite import Composite


class Factory(core.sql.compiling.Factory):
    def __init__(self, assembler: core.sql.compiling.IAssembler):
        super().__init__(assembler=Assembler(delegate=assembler))

    def make_composite(self) -> core.sql.compiling.IComposite | IComposite:
        return Composite(delegate=super().make_composite())
