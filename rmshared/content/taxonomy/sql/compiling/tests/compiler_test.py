from textwrap import dedent

from pytest import fixture

from rmshared.content.taxonomy import core
from rmshared.content.taxonomy import posts
from rmshared.content.taxonomy import users
from rmshared.content.taxonomy import variables

from rmshared.typings import read_only

from rmshared.content.taxonomy.sql.compiling.compiler import Compiler


class TestCompiler:
    @fixture
    def compiler(self) -> Compiler:
        return Compiler()

    def test_it_should_compile_any_badge_label_filter(self, compiler: Compiler):
        tree = compiler.make_tree_from_constant_filter(core.filters.AnyLabel(labels=(
            core.labels.Badge(field=posts.fields.IsPrivate()),
        )))
        assert self._compile_sql(tree) == 'is_private'

    def test_it_should_compile_no_badge_labels_filter(self, compiler: Compiler):
        tree = compiler.make_tree_from_constant_filter(core.filters.NoLabels(labels=(
            core.labels.Badge(field=posts.fields.IsPrivate()),
        )))
        assert self._compile_sql(tree) == 'NOT is_private'

    def test_it_should_compile_any_empty_label_filter(self, compiler: Compiler):
        tree = compiler.make_tree_from_constant_filter(core.filters.AnyLabel(labels=(
            core.labels.Empty(field=posts.fields.PrimarySection()),
            core.labels.Empty(field=posts.fields.RegularSection()),
        )))
        assert self._compile_sql(tree) == '( primary_section IS NULL OR regular_sections IS EMPTY )'

    def test_it_should_compile_no_empty_labels_filter(self, compiler: Compiler):
        tree = compiler.make_tree_from_constant_filter(core.filters.NoLabels(labels=(
            core.labels.Empty(field=posts.fields.PrimarySection()),
            core.labels.Empty(field=posts.fields.RegularSection()),
        )))
        assert self._compile_sql(tree) == 'primary_section IS NOT NULL AND regular_sections IS NOT EMPTY'

    def test_it_should_compile_any_value_label_filter_single(self, compiler: Compiler):
        tree = compiler.make_tree_from_constant_filter(core.filters.AnyLabel(labels=(
            core.labels.Value(field=posts.fields.Status(), value='published'),
        )))
        assert self._compile_sql(tree) == "status IS 'published'"

    def test_it_should_compile_any_value_label_filter_multiple(self, compiler: Compiler):
        tree = compiler.make_tree_from_constant_filter(core.filters.AnyLabel(labels=(
            core.labels.Value(field=posts.fields.Status(), value='published'),
            core.labels.Value(field=posts.fields.Status(), value='draft'),
        )))
        assert self._compile_sql(tree) == "status IN ('published', 'draft')"

    def test_it_should_compile_any_range_filter_with_multiple_ranges(self, compiler: Compiler):
        tree = compiler.make_tree_from_constant_filter(core.filters.AnyRange(ranges=(
            core.ranges.Between(field=posts.fields.CustomField(path='score'), min_value=0, max_value=50),
            core.ranges.MoreThan(field=posts.fields.CustomField(path='score'), value=100),
        )))
        assert self._compile_sql(tree) == "( CUSTOM_FIELD('score') BETWEEN 0 AND 50 OR CUSTOM_FIELD('score') > 100 )"

    def test_it_should_compile_any_less_than_range_filter(self, compiler: Compiler):
        tree = compiler.make_tree_from_constant_filter(core.filters.AnyRange(ranges=(
            core.ranges.LessThan(field=posts.fields.CustomField(path='numeric.field'), value=100),
        )))
        assert self._compile_sql(tree) == "CUSTOM_FIELD('numeric.field') < 100"

    def test_it_should_compile_any_more_than_range_filter(self, compiler: Compiler):
        tree = compiler.make_tree_from_constant_filter(core.filters.AnyRange(ranges=(
            core.ranges.MoreThan(field=posts.fields.CustomField(path='score.field'), value=50),
        )))
        assert self._compile_sql(tree) == "CUSTOM_FIELD('score.field') > 50"

    def test_it_should_compile_any_between_range_filter(self, compiler: Compiler):
        tree = compiler.make_tree_from_constant_filter(core.filters.AnyRange(ranges=(
            core.ranges.Between(field=posts.fields.CustomField(path='rating'), min_value=1, max_value=5),
        )))
        assert self._compile_sql(tree) == "CUSTOM_FIELD('rating') BETWEEN 1 AND 5"

    def test_it_should_compile_no_between_ranges_filter(self, compiler: Compiler):
        tree = compiler.make_tree_from_constant_filter(core.filters.NoRanges(ranges=(
            core.ranges.Between(field=posts.fields.CustomField(path='blocked.score'), min_value=10, max_value=20),
        )))
        assert self._compile_sql(tree) == "NOT CUSTOM_FIELD('blocked.score') BETWEEN 10 AND 20"

    def test_it_should_compile_no_less_than_ranges_filter(self, compiler: Compiler):
        tree = compiler.make_tree_from_constant_filter(core.filters.NoRanges(ranges=(
            core.ranges.LessThan(field=posts.fields.CustomField(path='min.threshold'), value=100),
        )))
        assert self._compile_sql(tree) == "CUSTOM_FIELD('min.threshold') >= 100"

    def test_it_should_compile_no_more_than_ranges_filter(self, compiler: Compiler):
        tree = compiler.make_tree_from_constant_filter(core.filters.NoRanges(ranges=(
            core.ranges.MoreThan(field=posts.fields.CustomField(path='max.threshold'), value=50),
        )))
        assert self._compile_sql(tree) == "CUSTOM_FIELD('max.threshold') <= 50"

    def test_it_should_compile_no_value_labels_filter_single(self, compiler: Compiler):
        tree = compiler.make_tree_from_constant_filter(core.filters.NoLabels(labels=(
            core.labels.Value(field=posts.fields.Status(), value='deprecated'),
        )))
        assert self._compile_sql(tree) == "status IS NOT 'deprecated'"

    def test_it_should_compile_no_value_labels_filter_multiple(self, compiler: Compiler):
        tree = compiler.make_tree_from_constant_filter(core.filters.NoLabels(labels=(
            core.labels.Value(field=posts.fields.Status(), value='deprecated'),
            core.labels.Value(field=posts.fields.Status(), value='obsolete'),
        )))
        assert self._compile_sql(tree) == "status NOT IN ('deprecated', 'obsolete')"

    def test_it_should_compile_any_labels_filter_with_single_multi_value_field(self, compiler: Compiler):
        tree = compiler.make_tree_from_constant_filter(core.filters.AnyLabel(labels=(
            core.labels.Value(field=posts.fields.RegularTag(), value='featured'),
        )))
        assert self._compile_sql(tree) == "regular_tags CONTAIN 'featured'"

    def test_it_should_compile_any_labels_filter_with_multiple_multi_value_field(self, compiler: Compiler):
        tree = compiler.make_tree_from_constant_filter(core.filters.AnyLabel(labels=(
            core.labels.Value(field=posts.fields.RegularTag(), value='featured'),
            core.labels.Value(field=posts.fields.RegularTag(), value='trending'),
        )))
        assert self._compile_sql(tree) == "regular_tags CONTAIN ANY ('featured', 'trending')"

    def test_it_should_compile_no_labels_filter_with_single_multi_value_field(self, compiler: Compiler):
        tree = compiler.make_tree_from_constant_filter(core.filters.NoLabels(labels=(
            core.labels.Value(field=posts.fields.RegularTag(), value='deprecated'),
        )))
        assert self._compile_sql(tree) == "regular_tags NOT CONTAIN 'deprecated'"

    def test_it_should_compile_no_labels_filter_with_multiple_multi_value_field(self, compiler: Compiler):
        tree = compiler.make_tree_from_constant_filter(core.filters.NoLabels(labels=(
            core.labels.Value(field=posts.fields.RegularTag(), value='deprecated'),
            core.labels.Value(field=posts.fields.RegularTag(), value='obsolete'),
        )))
        assert self._compile_sql(tree) == "regular_tags CONTAIN NONE ('deprecated', 'obsolete')"

    def test_it_should_compile_no_ranges_filter(self, compiler: Compiler):
        tree = compiler.make_tree_from_constant_filter(core.filters.NoRanges(ranges=(
            core.ranges.Between(
                field=posts.fields.CustomField(path='blocked.range'),
                min_value=10,
                max_value=20,
            ),
        )))
        assert self._compile_sql(tree) == "NOT CUSTOM_FIELD('blocked.range') BETWEEN 10 AND 20"

    def test_it_should_compile_return_operator_filter_with_constant(self, compiler: Compiler):
        tree = compiler.make_tree_from_variable_filter(variables.operators.Return(cases=(
            core.filters.AnyLabel(labels=(
                variables.operators.Return(cases=(
                    core.labels.Value(
                        field=posts.fields.Status(),
                        value=variables.values.Constant(value='draft'),
                    ),
                )),
            )),
        )))
        assert self._compile_sql(tree) == "status IS 'draft'"

    def test_it_should_compile_return_operator_filter_with_variable(self, compiler: Compiler):
        tree = compiler.make_tree_from_variable_filter(variables.operators.Return(cases=(
            core.filters.AnyLabel(labels=(
                variables.operators.Return(cases=(
                    core.labels.Value(
                        field=posts.fields.Status(),
                        value=variables.values.Variable(
                            ref=variables.Reference(alias='post_status'),
                            index=0
                        ),
                    ),
                )),
            )),
        )))
        assert self._compile_sql(tree) == "status IS @post_status"

    def test_it_should_compile_switch_operator_filter(self, compiler: Compiler):
        tree = compiler.make_tree_from_variable_filter(variables.operators.Switch(
            ref=variables.Reference(alias='tag_slug'),
            cases=read_only({
                variables.arguments.Any: variables.operators.Return(cases=(
                    core.filters.AnyLabel(labels=(
                        variables.operators.Return(cases=(
                            core.labels.Empty(field=posts.fields.RegularTag()),
                        )),
                    )),
                )),
                variables.arguments.Value: variables.operators.Return(cases=(
                    core.filters.NoLabels(labels=(
                        variables.operators.Return(cases=(
                            core.labels.Value(
                                field=posts.fields.RegularTag(),
                                value=variables.values.Variable(
                                    ref=variables.Reference(alias='tag_slug'),
                                    index=0
                                ),
                            ),
                        )),
                    )),
                )),
            })
        ))
        assert self._compile_sql(tree) == 'regular_tags NOT CONTAIN @tag_slug IF @tag_slug IS NOT NULL OTHERWISE regular_tags IS EMPTY'

    def test_it_should_compile_switch_operator_filter_value_only(self, compiler: Compiler):
        tree = compiler.make_tree_from_variable_filter(variables.operators.Switch(
            ref=variables.Reference(alias='status_filter'),
            cases=read_only({
                variables.arguments.Value: variables.operators.Return(cases=(
                    core.filters.AnyLabel(labels=(
                        variables.operators.Return(cases=(
                            core.labels.Value(
                                field=posts.fields.Status(),
                                value=variables.values.Variable(
                                    ref=variables.Reference(alias='status_filter'),
                                    index=0
                                ),
                            ),
                        )),
                    )),
                )),
            })
        ))
        assert self._compile_sql(tree) == 'status IS @status_filter IF @status_filter IS NOT NULL'

    def test_it_should_compile_switch_operator_filter_any_only(self, compiler: Compiler):
        tree = compiler.make_tree_from_variable_filter(variables.operators.Switch(
            ref=variables.Reference(alias='category_check'),
            cases=read_only({
                variables.arguments.Any: variables.operators.Return(cases=(
                    core.filters.AnyLabel(labels=(
                        variables.operators.Return(cases=(
                            core.labels.Empty(field=posts.fields.PrimarySection()),
                        )),
                    )),
                )),
            })
        ))
        assert self._compile_sql(tree) == 'primary_section IS NULL IF @category_check IS NULL'


    def test_it_should_compile_field(self, compiler: Compiler):
        tree = compiler.make_tree_from_field(posts.fields.Title())
        assert self._compile_sql(tree) == 'title'

    def test_it_should_compile_custom_field(self, compiler: Compiler):
        tree = compiler.make_tree_from_field(posts.fields.CustomField(path='nested.field.path'))
        assert self._compile_sql(tree) == "CUSTOM_FIELD('nested.field.path')"


    def test_it_should_compile_event(self, compiler: Compiler):
        tree = compiler.make_tree_from_event(posts.events.PageView())
        assert self._compile_sql(tree) == 'page_views'

    def test_it_should_compile_core_event(self, compiler: Compiler):
        tree = compiler.make_tree_from_event(core.events.Event('user-profile-page-view'))
        assert self._compile_sql(tree) == 'page_views'


    def test_it_should_compile_scalar_string(self, compiler: Compiler):
        tree = compiler.make_tree_from_scalar('test_value')
        assert self._compile_sql(tree) == "'test_value'"

    def test_it_should_compile_scalar_integer(self, compiler: Compiler):
        tree = compiler.make_tree_from_scalar(42)
        assert self._compile_sql(tree) == '42'

    def test_it_should_compile_scalar_float(self, compiler: Compiler):
        tree = compiler.make_tree_from_scalar(3.14)
        assert self._compile_sql(tree) == '3.14'


    def test_it_should_compile_variable_reference(self, compiler: Compiler):
        tree = compiler.make_tree_from_variable_reference(variables.Reference(alias='my_variable'))
        assert self._compile_sql(tree) == '@my_variable'


    def test_it_should_compile_scope(self, compiler: Compiler):
        tree = compiler.make_tree_from_scope(posts.guids.Post)
        assert self._compile_sql(tree) == 'posts'

    def test_it_should_compile_id_field(self, compiler: Compiler):
        tree = compiler.make_tree_from_id_field(users.guids.UserProfile)
        assert self._compile_sql(tree) == 'profile.id'

    @staticmethod
    def _compile_sql(tree) -> str:
        return ''.join(tree.compile())

    @staticmethod
    def _normalize_sql(sql: str) -> str:
        return dedent(sql).strip()
