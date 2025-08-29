from __future__ import annotations

from ast import literal_eval

from lark import Token
from lark import visitors

from rmshared.sql.parsing.lark.ext import read_grammar_lazy
from rmshared.sql.parsing.lark.ext import visit_children


class Interpreter(visitors.Interpreter):
    GRAMMAR = read_grammar_lazy('grammar.lark')

    @staticmethod
    @visit_children
    def string(token: Token) -> str:
        return literal_eval(token.value)

    @staticmethod
    @visit_children
    def number(number: Token) -> int | float:
        if '.' in number.value:
            return float(number.value)
        else:
            return int(number.value)
