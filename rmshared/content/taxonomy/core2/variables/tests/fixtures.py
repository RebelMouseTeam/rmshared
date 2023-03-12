from rmshared.typings import read_only

from rmshared.content.taxonomy.core2 import filters
from rmshared.content.taxonomy.core2 import labels
from rmshared.content.taxonomy.core2 import ranges
from rmshared.content.taxonomy.core2 import fields
from rmshared.content.taxonomy.core2.variables import values
from rmshared.content.taxonomy.core2.variables import arguments
from rmshared.content.taxonomy.core2.variables import operators
from rmshared.content.taxonomy.core2.variables.abc import Reference

FILTERS = tuple([
    operators.Return[filters.Filter](
        cases=(
            filters.AnyLabel(labels=(
                operators.Return[labels.Label](cases=(
                    labels.Value(field=fields.System('post-id'), value=values.Constant(123)),
                )),
            )),
        ),
    ),
    operators.Switch[filters.Filter](
        ref=Reference('$1'),
        cases=read_only({
            arguments.Empty: operators.Return[filters.Filter](cases=(
                filters.AnyLabel(labels=(
                    operators.Return[labels.Label](cases=(
                        labels.Empty(field=fields.System('post-regular-section')),
                    )),
                )),
            )),
            arguments.Value: operators.Return[filters.Filter](cases=(
                filters.AnyLabel(labels=(
                    operators.Return[labels.Label](cases=(
                        labels.Value(field=fields.System('post-regular-section'), value=values.Variable(ref=Reference('$1'), index=1)),
                    )),
                )),
            )),
        }),
    ),
    operators.Switch[filters.Filter](
        ref=Reference('$2'),
        cases=read_only({
            arguments.Any: operators.Return(cases=()),
            arguments.Empty: operators.Return[filters.Filter](cases=(
                filters.NoLabels(labels=(
                    operators.Return[labels.Label](cases=(
                        labels.Badge(field=fields.System('private-post')),
                    )),
                )),
            )),
            arguments.Value: operators.Return[filters.Filter](cases=(
                filters.AnyLabel(labels=(
                    operators.Return[labels.Label](cases=(
                        labels.Badge(field=fields.System('private-post')),
                    )),
                )),
            )),
        }),
    ),
    operators.Return[filters.Filter](
        cases=(
            filters.AnyLabel(labels=(
                operators.Return[labels.Label](cases=(
                    labels.Value(field=fields.System('post-id'), value=values.Constant(123)),
                )),
                operators.Switch[labels.Label](
                    ref=Reference('$3'),
                    cases=read_only({
                        arguments.Empty: operators.Return[labels.Label](cases=(
                            labels.Empty(field=fields.System('post-primary-tag')),
                        )),
                        arguments.Value: operators.Return[labels.Label](cases=(
                            labels.Value(field=fields.System('post-primary-tag'), value=values.Variable(ref=Reference('$3'), index=1)),
                            labels.Value(field=fields.System('post-primary-tag'), value=values.Variable(ref=Reference('$3'), index=2)),
                        )),
                    }),
                ),
            )),
        ),
    ),
    operators.Switch[filters.Filter](
        ref=Reference('$4'),
        cases=read_only({
            arguments.Value: operators.Return[filters.Filter](cases=(
                filters.AnyRange(ranges=(
                    operators.Return[ranges.Range](cases=(
                        ranges.Between(
                            field=fields.System('post-modified-at'),
                            min_value=values.Variable(ref=Reference('$4'), index=2),
                            max_value=values.Variable(ref=Reference('$5'), index=1)
                        ),
                    )),
                )),
            )),
        }),
    ),
    operators.Return[filters.Filter](
        cases=(
            filters.NoRanges(ranges=(
                operators.Switch[ranges.Range](
                    ref=Reference('$5'),
                    cases=read_only({
                        arguments.Value: operators.Return[ranges.Range](cases=(
                            ranges.MoreThan[fields.Field, values.Value](
                                field=fields.System('post-modified-at'),
                                value=values.Variable(ref=Reference('$4'), index=1),
                            ),
                            ranges.Between[fields.Field, values.Value](
                                field=fields.System('post-published-at'),
                                min_value=values.Constant(100),
                                max_value=values.Variable(ref=Reference('$5'), index=2),
                            ),
                        )),
                    }),
                ),
            )),
        ),
    ),
])
