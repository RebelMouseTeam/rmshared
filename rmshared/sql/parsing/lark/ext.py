import inspect
import os

from collections.abc import Callable
from collections.abc import Iterator
from collections.abc import Sequence
from typing import Generic
from typing import TypeVar

from lark import Tree
from lark import Token
from lark import v_args
from lark.tree import Meta

from rmshared.tools import group_to_mapping

from rmshared.sql import exceptions
from rmshared.sql.parsing.lark.lazy import LazyGrammar

T = TypeVar('T')

__all__ = (
    'read_grammar',
    'read_grammar_lazy',

    'visit_tree',
    'visit_none',
    'visit_rules',
    'visit_tokens',
    'visit_children',

    'group_rules',
)


def read_grammar(filename: str, caller_file=None) -> str:
    with open(_find_file(filename, caller_file), 'r') as file:
        return file.read()


def read_grammar_lazy(filename: str, caller_file=None) -> LazyGrammar:
    return LazyGrammar(filename=_find_file(filename, caller_file))


def _find_file(filename: str, caller_file: str = None) -> str:
    if caller_file is None:
        caller_frame = inspect.stack()[1]
        caller_file = caller_frame.filename

    return os.path.join(os.path.dirname(caller_file), filename)


class WrapperProtocol(Callable):
    def __call__(self, func: Callable[[...], T], rule: str, children: Sequence[Tree | Token], meta: Meta) -> T:
        ...


class VisitTreeWrapper(WrapperProtocol, Generic[T]):
    def __call__(self, func, rule, children, meta) -> T:
        try:
            return func(Tree(rule, list(children), meta))
        except exceptions.InterpreterError:
            raise
        except Exception as e:
            raise exceptions.InterpreterError(rule, meta.line, meta.column, meta.end_line, meta.end_column, original=e) from e


class VisitChildrenWrapper(WrapperProtocol, Generic[T]):
    def __init__(self, filter_func: Callable[[Tree | Token], bool]):
        self.filter_func = filter_func

    def __call__(self, func, rule, children, meta) -> T:
        try:
            return func(*filter(self.filter_func, children))
        except exceptions.InterpreterError:
            raise
        except Exception as e:
            raise exceptions.InterpreterError(rule, meta.line, meta.column, meta.end_line, meta.end_column, original=e) from e


visit_tree = v_args(wrapper=VisitTreeWrapper())
visit_none = v_args(wrapper=VisitChildrenWrapper(filter_func=lambda _: False))
visit_rules = v_args(wrapper=VisitChildrenWrapper(filter_func=lambda child: isinstance(child, Tree)))
visit_tokens = v_args(wrapper=VisitChildrenWrapper(filter_func=lambda child: isinstance(child, Token)))
visit_children = v_args(wrapper=VisitChildrenWrapper(filter_func=lambda _: True))


class GroupRulesWrapper(WrapperProtocol, Generic[T]):
    def __init__(self, rules: Sequence[str]):
        self.rules = rules

    def __call__(self, func, rule, children, meta) -> T:
        try:
            return func(*self._group_children_by_rules(children))
        except exceptions.InterpreterError:
            raise
        except Exception as e:
            raise exceptions.InterpreterError(rule, meta.line, meta.column, meta.end_line, meta.end_column, original=e) from e

    def _group_children_by_rules(self, children: Sequence[Tree | Token]) -> Iterator[Sequence[Tree] | Sequence[Token]]:
        rule_to_children_map = group_to_mapping(children, key_func=self._get_rule_name_or_token_type)
        return map(lambda rule_: rule_to_children_map.get(rule_, []), self.rules)

    @staticmethod
    def _get_rule_name_or_token_type(child: Tree | Token) -> str:
        if isinstance(child, Tree):
            return child.data
        elif isinstance(child, Token):
            return child.type
        else:
            raise TypeError(f'Expected Tree or Token, got {type(child)}')


def group_rules(*rules: str):
    return v_args(wrapper=GroupRulesWrapper(rules))
