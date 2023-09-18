from rmshared.typings import read_only

from rmshared.content.taxonomy.core import filters
from rmshared.content.taxonomy.core import labels
from rmshared.content.taxonomy.core import ranges
from rmshared.content.taxonomy.core import fields
from rmshared.content.taxonomy.variables import values
from rmshared.content.taxonomy.variables import arguments
from rmshared.content.taxonomy.variables import operators
from rmshared.content.taxonomy.variables.abc import Reference

FILTERS = tuple([
    operators.Return[filters.Filter](cases=(
        filters.AnyLabel[operators.Operator[labels.Label]](labels=(
            operators.Return[labels.Label](cases=(
                labels.Value(field=fields.System('post-id'), value=values.Constant(123)),
            )),
        )),
    )),
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
            arguments.Any: operators.Return[filters.Filter](cases=()),
            arguments.Empty: operators.Return[filters.Filter](cases=(
                filters.NoLabels(labels=(
                    operators.Return[labels.Label](cases=(
                        labels.Empty(field=fields.System('private-post')),
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
    operators.Switch[filters.Filter](
        ref=Reference('$3'),
        cases=read_only({
            arguments.Any: operators.Return[filters.Filter](cases=(
                filters.AnyLabel(labels=(
                    operators.Return[labels.Label](cases=(
                        labels.Value(field=fields.System('post-id'), value=values.Constant(123)),
                    )),
                )),
            )),
            arguments.Empty: operators.Return[filters.Filter](cases=(
                filters.AnyLabel(labels=(
                    operators.Return[labels.Label](cases=(
                        labels.Value(field=fields.System('post-id'), value=values.Constant(123)),
                    )),
                    operators.Return[labels.Label](cases=(
                        labels.Empty(field=fields.System('post-primary-tag')),
                    )),
                )),
            )),
            arguments.Value: operators.Return[filters.Filter](cases=(
                filters.AnyLabel(labels=(
                    operators.Return[labels.Label](cases=(
                        labels.Value(field=fields.System('post-id'), value=values.Constant(123)),
                    )),
                    operators.Return[labels.Label](cases=(
                        labels.Value(field=fields.System('post-primary-tag'), value=values.Variable(ref=Reference('$3'), index=1)),
                    )),
                    operators.Return[labels.Label](cases=(
                        labels.Value(field=fields.System('post-primary-tag'), value=values.Variable(ref=Reference('$3'), index=2)),
                    )),
                )),
            )),
        }),
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
    operators.Switch[filters.Filter](
        ref=Reference('$5'),
        cases=read_only({
            arguments.Value: operators.Return[filters.Filter](cases=(
                filters.NoRanges(ranges=(
                    operators.Return[ranges.Range](cases=(
                        ranges.MoreThan[fields.Field, values.Value](
                            field=fields.System('post-modified-at'),
                            value=values.Variable(ref=Reference('$4'), index=1),
                        ),
                    )),
                    operators.Return[ranges.Range](cases=(
                        ranges.Between[fields.Field, values.Value](
                            field=fields.System('post-published-at'),
                            min_value=values.Constant(100),
                            max_value=values.Variable(ref=Reference('$5'), index=2),
                        ),
                    )),
                )),
            )),
        }),
    ),
])
