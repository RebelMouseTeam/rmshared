from rmshared.typings import read_only

from rmshared.content.taxonomy import core
from rmshared.content.taxonomy.variables import values
from rmshared.content.taxonomy.variables import arguments
from rmshared.content.taxonomy.variables import operators
from rmshared.content.taxonomy.variables.abc import Reference

FILTERS = tuple([
    operators.Return(cases=(
        core.filters.AnyLabel(labels=(
            operators.Return(cases=(
                core.labels.Value(field=core.fields.System('post-id'), value=values.Constant(123)),
            )),
        )),
    )),
    operators.Switch(
        ref=Reference('variable_1'),
        cases=read_only({
            arguments.Empty: operators.Return(cases=(
                core.filters.AnyLabel(labels=(
                    operators.Return(cases=(
                        core.labels.Empty(field=core.fields.System('post-regular-section')),
                    )),
                )),
            )),
            arguments.Value: operators.Return(cases=(
                core.filters.AnyLabel(labels=(
                    operators.Return(cases=(
                        core.labels.Value(field=core.fields.System('post-regular-section'), value=values.Variable(ref=Reference('variable_1'), index=1)),
                    )),
                )),
            )),
        }),
    ),
    operators.Switch(
        ref=Reference('$2'),
        cases=read_only({
            arguments.Any: operators.Return(cases=()),
            arguments.Empty: operators.Return(cases=(
                core.filters.NoLabels(labels=(
                    operators.Return(cases=(
                        core.labels.Empty(field=core.fields.System('private-post')),
                    )),
                )),
            )),
            arguments.Value: operators.Return(cases=(
                core.filters.AnyLabel(labels=(
                    operators.Return(cases=(
                        core.labels.Badge(field=core.fields.System('private-post')),
                    )),
                )),
            )),
        }),
    ),
    operators.Switch(
        ref=Reference('$3'),
        cases=read_only({
            arguments.Any: operators.Return(cases=(
                core.filters.AnyLabel(labels=(
                    operators.Return(cases=(
                        core.labels.Value(field=core.fields.System('post-id'), value=values.Constant(123)),
                    )),
                )),
            )),
            arguments.Empty: operators.Return(cases=(
                core.filters.AnyLabel(labels=(
                    operators.Return(cases=(
                        core.labels.Value(field=core.fields.System('post-id'), value=values.Constant(123)),
                    )),
                    operators.Return(cases=(
                        core.labels.Empty(field=core.fields.System('post-primary-tag')),
                    )),
                )),
            )),
            arguments.Value: operators.Return(cases=(
                core.filters.AnyLabel(labels=(
                    operators.Return(cases=(
                        core.labels.Value(field=core.fields.System('post-id'), value=values.Constant(123)),
                    )),
                    operators.Return(cases=(
                        core.labels.Value(field=core.fields.System('post-primary-tag'), value=values.Variable(ref=Reference('$3'), index=1)),
                    )),
                    operators.Return(cases=(
                        core.labels.Value(field=core.fields.System('post-primary-tag'), value=values.Variable(ref=Reference('$3'), index=2)),
                    )),
                )),
            )),
        }),
    ),
    operators.Switch(
        ref=Reference('$4'),
        cases=read_only({
            arguments.Value: operators.Return(cases=(
                core.filters.AnyRange(ranges=(
                    operators.Return(cases=(
                        core.ranges.Between(
                            field=core.fields.System('post-modified-at'),
                            min_value=values.Variable(ref=Reference('$4'), index=2),
                            max_value=values.Variable(ref=Reference('$5'), index=1)
                        ),
                    )),
                )),
            )),
        }),
    ),
    operators.Switch(
        ref=Reference('$5'),
        cases=read_only({
            arguments.Value: operators.Return(cases=(
                core.filters.NoRanges(ranges=(
                    operators.Return(cases=(
                        core.ranges.MoreThan(
                            field=core.fields.System('post-modified-at'),
                            value=values.Variable(ref=Reference('$4'), index=1),
                        ),
                    )),
                    operators.Return(cases=(
                        core.ranges.Between(
                            field=core.fields.System('post-published-at'),
                            min_value=values.Constant(100),
                            max_value=values.Variable(ref=Reference('$5'), index=2),
                        ),
                    )),
                )),
            )),
        }),
    ),
])
