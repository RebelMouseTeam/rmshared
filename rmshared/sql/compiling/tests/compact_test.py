from rmshared.sql.compiling import compact
from rmshared.sql.compiling.compact import Break


class TestWithConnector:
    def test_with_custom_connector(self):
        @compact.with_connector(' | ')
        def generate_tokens():
            yield 'a'
            yield 'b'
            yield 'c'

        result = list(generate_tokens())
        assert result == ['a | b | c']

    def test_with_empty_connector(self):
        @compact.with_connector('')
        def generate_tokens():
            yield 'hello'
            yield 'world'

        result = list(generate_tokens())
        assert result == ['helloworld']

    def test_with_space(self):
        @compact.with_space
        def generate_tokens():
            yield 'SELECT'
            yield 'column'
            yield 'FROM'
            yield 'table'

        result = list(generate_tokens())
        assert result == ['SELECT column FROM table']

    def test_with_comma(self):
        @compact.with_comma
        def generate_tokens():
            yield 'a'
            yield 'b'
            yield 'c'

        result = list(generate_tokens())
        assert result == ['a, b, c']

    def test_with_new_line(self):
        @compact.with_new_line
        def generate_tokens():
            yield 'line1'
            yield 'line2'

        result = list(generate_tokens())
        assert result == ['line1\nline2']

    def test_with_indent(self):
        @compact.with_indent
        def generate_tokens():
            yield 'first'
            yield 'second'

        result = list(generate_tokens())
        assert result == ['first\n    second']

    def test_with_nothing(self):
        @compact.with_nothing
        def generate_tokens():
            yield 'a'
            yield 'b'
            yield 'c'

        result = list(generate_tokens())
        assert result == ['abc']

    def test_with_breaks(self):
        @compact.with_space
        def generate_tokens():
            yield 'before'
            yield Break()
            yield 'after'

        result = list(generate_tokens())
        assert len(result) == 3
        assert result[0] == 'before'
        assert isinstance(result[1], Break)
        assert result[2] == 'after'


class TestBreaksAs:
    def test_breaks_replacement(self):
        @compact.breaks_as('\n')
        def generate_tokens():
            yield 'line1'
            yield Break()
            yield 'line2'

        result = list(generate_tokens())
        assert result == ['line1\nline2']

    def test_multiple_breaks(self):
        @compact.breaks_as(' -- ')
        def generate_tokens():
            yield 'a'
            yield Break()
            yield 'b'
            yield Break()
            yield 'c'

        result = list(generate_tokens())
        assert result == ['a -- b -- c']


class TestBreak:
    def test_break_creation(self):
        break_obj = Break()
        assert isinstance(break_obj, str)
        assert break_obj == ' '

    def test_break_is_instance(self):
        break_obj = Break()
        assert isinstance(break_obj, Break)
