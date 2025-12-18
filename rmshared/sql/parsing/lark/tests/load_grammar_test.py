from collections.abc import Iterator

from pathlib import Path
from tempfile import TemporaryDirectory

from pytest import fixture

from rmshared.sql.parsing.lark.ext import read_grammar_lazy
from rmshared.sql.parsing.lark.lazy import LazyGrammar


class TestReadGrammarLazy:
    @fixture
    def caller_file(self, grammar_path: str) -> str:
        return str(Path(grammar_path).parent / 'dummy.py')

    @fixture
    def grammar_path(self) -> Iterator[str]:
        with TemporaryDirectory() as temp_dir:
            grammar_path = Path(temp_dir) / 'test.lark'
            grammar_path.write_text('start: "hello" "world"\n')
            yield str(grammar_path)

    def test_read_grammar_lazy_should_resolve_relative_path_from_caller_file(self, grammar_path, caller_file):
        result = read_grammar_lazy(grammar_path, caller_file=str(caller_file))
        assert isinstance(result, LazyGrammar)
        assert ' !!! '.join(['start', str(result), 'finish']) == 'start !!! start: "hello" "world"\n !!! finish'
