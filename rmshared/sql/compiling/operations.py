from abc import ABCMeta
from abc import abstractmethod

from rmshared.sql.compiling.abc import ITree


class UnaryOperation(ITree, metaclass=ABCMeta):
    def __init__(self, operand: ITree):
        self.operand = operand

    def compile(self):
        yield from self.operand.compile()
        yield self.operator

    @property
    @abstractmethod
    def operator(self) -> str:
        ...


class IsTrue(UnaryOperation):
    @property
    def operator(self) -> str:
        return 'IS TRUE'


class IsFalse(UnaryOperation):
    @property
    def operator(self) -> str:
        return 'IS FALSE'


class IsNull(UnaryOperation):
    @property
    def operator(self) -> str:
        return 'IS NULL'


class IsNotNull(UnaryOperation):
    @property
    def operator(self) -> str:
        return 'IS NOT NULL'


class IsEmpty(UnaryOperation):
    @property
    def operator(self) -> str:
        return 'IS EMPTY'


class IsNotEmpty(UnaryOperation):
    @property
    def operator(self) -> str:
        return 'IS NOT EMPTY'


class BinaryOperation(ITree, metaclass=ABCMeta):
    def __init__(self, operand_1: ITree, operand_2: ITree):
        self.operand_1 = operand_1
        self.operand_2 = operand_2

    def compile(self):
        yield from self.operand_1.compile()
        yield self.operator
        yield from self.operand_2.compile()

    @property
    @abstractmethod
    def operator(self) -> str:
        ...


class IsEqual(BinaryOperation):
    @property
    def operator(self) -> str:
        return 'IS'


class IsNotEqual(BinaryOperation):
    @property
    def operator(self) -> str:
        return 'IS NOT'


class IsIn(BinaryOperation):
    @property
    def operator(self) -> str:
        return 'IN'


class IsNotIn(BinaryOperation):
    @property
    def operator(self) -> str:
        return 'NOT IN'


class Contain(BinaryOperation):
    @property
    def operator(self) -> str:
        return 'CONTAIN'


class NotContain(BinaryOperation):
    @property
    def operator(self) -> str:
        return 'NOT CONTAIN'


class ContainAny(BinaryOperation):
    @property
    def operator(self) -> str:
        return 'CONTAIN ANY'


class ContainNone(BinaryOperation):
    @property
    def operator(self) -> str:
        return 'CONTAIN NONE'


class IsMoreThan(BinaryOperation):
    @property
    def operator(self) -> str:
        return '>'


class IsLessThan(BinaryOperation):
    @property
    def operator(self) -> str:
        return '<'


class IsMoreThanOrEqual(BinaryOperation):
    @property
    def operator(self) -> str:
        return '>='


class IsLessThanOrEqual(BinaryOperation):
    @property
    def operator(self) -> str:
        return '<='


class Between(ITree):
    def __init__(self, operand: ITree, lower_bound: ITree, upper_bound: ITree):
        self.operand = operand
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def compile(self):
        yield from self.operand.compile()
        yield 'BETWEEN'
        yield from self.lower_bound.compile()
        yield 'AND'
        yield from self.upper_bound.compile()


class ItemGetter(ITree):
    def __init__(self, name: ITree, item: ITree):
        self.name = name
        self.item = item

    def compile(self):
        yield from self.name.compile()
        yield '['
        yield from self.item.compile()
        yield ']'
