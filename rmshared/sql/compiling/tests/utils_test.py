from rmshared.sql.compiling import compact
from rmshared.sql.compiling.utils import CommaSeparatedList
from rmshared.sql.compiling.utils import CommaSeparatedLines
from rmshared.sql.compiling.utils import Wrapped
from rmshared.sql.compiling.utils import Joined
from rmshared.sql.compiling.utils import Chain
from rmshared.sql.compiling.utils import Compacted
from rmshared.sql.compiling.terminals import CName
from rmshared.sql.compiling.terminals import String


class TestCommaSeparatedList:
    def test_single_item(self):
        item = CName('column')
        csv_list = CommaSeparatedList([item])

        result = list(csv_list.compile())
        assert result == ['column']

    def test_multiple_items(self):
        items = [CName('col1'), CName('col2'), CName('col3')]
        csv_list = CommaSeparatedList(items)

        result = list(csv_list.compile())
        assert result == ['col1', ', ', 'col2', ', ', 'col3']


class TestCommaSeparatedLines:
    def test_single_item(self):
        item = CName('line')
        csv_lines = CommaSeparatedLines([item])

        result = list(csv_lines.compile())
        assert result == ['line']

    def test_multiple_items(self):
        items = [CName('line1'), CName('line2')]
        csv_lines = CommaSeparatedLines(items)

        result = list(csv_lines.compile())
        assert result == ['line1', ',\n', 'line2']


class TestWrapped:
    def test_default_parentheses(self):
        content = CName('content')
        wrapped = Wrapped(content)

        result = list(wrapped.compile())
        assert result == ['(', 'content', ')']

    def test_custom_parentheses(self):
        content = CName('content')
        wrapped = Wrapped(content, parentheses='[]')

        result = list(wrapped.compile())
        assert result == ['[', 'content', ']']

    def test_custom_braces(self):
        content = CName('content')
        wrapped = Wrapped(content, parentheses='{}')

        result = list(wrapped.compile())
        assert result == ['{', 'content', '}']


class TestJoined:
    def test_with_space_separator(self):
        content = Chain(CName('SELECT'), CName('column'))
        joined = Joined(content, separator=' ')

        result = list(joined.compile())
        assert result == ['SELECT column']

    def test_with_comma_separator(self):
        content = Chain(CName('a'), CName('b'), CName('c'))
        joined = Joined(content, separator=',')

        result = list(joined.compile())
        assert result == ['a,b,c']


class TestChain:
    def test_empty_chain(self):
        chain = Chain()

        result = list(chain.compile())
        assert result == []

    def test_single_expression(self):
        chain = Chain(CName('single'))

        result = list(chain.compile())
        assert result == ['single']

    def test_multiple_expressions(self):
        chain = Chain(CName('first'), String('second'), CName('third'))

        result = list(chain.compile())
        assert result == ['first', "'second'", 'third']

    def test_from_iterable(self):
        expressions = [CName('a'), CName('b')]
        chain = Chain.from_iterable(expressions)

        result = list(chain.compile())
        assert result == ['a', 'b']


class TestCompacted:
    def test_with_space_decorator(self):
        content = Chain(CName('SELECT'), CName('column'))
        compacted = Compacted(content, compact.with_space)

        result = list(compacted.compile())
        assert result == ['SELECT column']

    def test_with_comma_decorator(self):
        content = Chain(CName('a'), CName('b'), CName('c'))
        compacted = Compacted(content, compact.with_comma)

        result = list(compacted.compile())
        assert result == ['a, b, c']
