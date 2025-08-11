from rmshared.sql.compiling.terminals import CName
from rmshared.sql.compiling.terminals import Keyword
from rmshared.sql.compiling.terminals import String
from rmshared.sql.compiling.terminals import Number
from rmshared.sql.compiling.terminals import ItemGetter
from rmshared.sql.compiling.terminals import Nothing
from rmshared.sql.compiling.terminals import Break


class TestCName:
    def test_compile(self):
        name = CName('table_name')
        result = list(name.compile())
        assert result == ['table_name']


class TestKeyword:
    def test_compile_uppercase(self):
        keyword = Keyword('select')

        result = list(keyword.compile())
        assert result == ['SELECT']
    
    def test_compile_mixed_case(self):
        keyword = Keyword('WhErE')

        result = list(keyword.compile())
        assert result == ['WHERE']


class TestString:
    def test_compile_default_quotes(self):
        string = String('hello world')

        result = list(string.compile())
        assert result == ["'hello world'"]
    
    def test_compile_with_single_quote_escape(self):
        string = String("it's working")

        result = list(string.compile())
        assert result == ["'it\\'s working'"]
    
    def test_compile_double_quotes_param(self):
        string = String('test', quotes=String.DOUBLE_QUOTE)

        result = list(string.compile())
        assert result == ["'test'"]


class TestNumber:
    def test_compile_integer(self):
        number = Number(42)

        result = list(number.compile())
        assert result == ['42']
    
    def test_compile_float(self):
        number = Number(3.14)

        result = list(number.compile())
        assert result == ['3.14']
    
    def test_compile_zero(self):
        number = Number(0)

        result = list(number.compile())
        assert result == ['0']


class TestItemGetter:
    def test_compile(self):
        ref = CName('array')
        index = Number(1)
        getter = ItemGetter(ref, index)

        result = list(getter.compile())
        assert result == ['array', '1']


class TestNothing:
    def test_compile(self):
        nothing = Nothing()
        result = list(nothing.compile())
        assert result == []


class TestBreak:
    def test_compile(self):
        break_obj = Break()

        result = list(break_obj.compile())
        from rmshared.sql.compiling.compact import Break as CompactBreak
        assert len(result) == 1
        assert isinstance(result[0], CompactBreak)
