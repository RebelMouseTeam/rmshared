from rmshared.content.taxonomy import core
from rmshared.content.taxonomy.sections import access
from rmshared.content.taxonomy.sections import consts
from rmshared.content.taxonomy.sections import labels
from rmshared.content.taxonomy.sections import fields


class TestMappers:
    def test_it_should_map_filters(self):
        assert tuple(self.CORE_FILTERS) == tuple(self.SECTIONS_FILTERS)

    SECTIONS_FILTERS = [
        core.filters.AnyLabel(labels=(
            labels.Id(value=123),
            labels.Slug(value='section-1'),
            labels.ReadOnly(),
            labels.ParentSlug(value='parent-slug-1'),
            labels.AncestorSlug(value='ancestor-slug-1'),
            labels.Visibility(value=consts.VISIBILITY.STATUS.UNLISTED),
            labels.AllowCommunityPosts(),
            labels.LockPostsAfterPublishing(),
            labels.NoImageId(),
            labels.LinkOut(value='https://example.com'),
            labels.NoCustomField(path='path.to.field_1'),
        )),
        core.filters.NoLabels(labels=(
            labels.Path(value='path/to/section-1'),
            labels.Title(value='Title #1'),
            labels.ParentId(value=234),
            labels.AncestorId(value=345),
            labels.ReadAccess(value=access.Restricted(is_inherited=False)),
            labels.OpenInNewTab(),
            labels.HideFromEntryEditor(),
            labels.ImageId(value=456),
            labels.NoLinkOut(),
            labels.CustomField(path='path.to.field_2', value='value-1'),
        )),
        core.filters.AnyRange[core.ranges.Range[core.fields.Field]](ranges=(
            core.ranges.Between(field=fields.Title(), min_value='A', max_value='Z'),
            core.ranges.LessThan(field=fields.OrderId(), value=30),
        )),
        core.filters.NoRanges[core.ranges.Range[core.fields.Field]](ranges=(
            core.ranges.MoreThan(field=fields.OrderId(), value=50),
            core.ranges.Between(field=fields.CustomField(path='path.to.field.3'), min_value=0.01, max_value=0.99),
        )),
    ]
    CORE_FILTERS = [
        core.filters.AnyLabel[core.labels.Label](labels=(
            core.labels.Value(field=core.fields.System(name='section-id'), value=123),
            core.labels.Value(field=core.fields.System(name='section-slug'), value='section-1'),
            core.labels.Badge(field=core.fields.System(name='section-is-read-only')),
            core.labels.Value(field=core.fields.System(name='section-parent-slug'), value='parent-slug-1'),
            core.labels.Value(field=core.fields.System(name='section-ancestor-slug'), value='ancestor-slug-1'),
            core.labels.Value(field=core.fields.System(name='section-visibility'), value='unlisted'),
            core.labels.Badge(field=core.fields.System(name='section-allow-community-posts-setting')),
            core.labels.Badge(field=core.fields.System(name='section-lock-posts-after-publishing-setting')),
            core.labels.Empty(field=core.fields.System(name='section-image-id')),
            core.labels.Value(field=core.fields.System(name='section-link-out'), value='https://example.com'),
            core.labels.Empty(field=core.fields.Custom(name='section-custom-field', path='path.to.field_1')),
        )),
        core.filters.NoLabels[core.labels.Label](labels=(
            core.labels.Value(field=core.fields.System(name='section-path'), value='path/to/section-1'),
            core.labels.Value(field=core.fields.System(name='section-title'), value='Title #1'),
            core.labels.Value(field=core.fields.System(name='section-parent-id'), value=234),
            core.labels.Value(field=core.fields.System(name='section-ancestor-id'), value=345),
            core.labels.Value(field=core.fields.System(name='section-read-access-kind'), value='restricted(inherited=false)'),
            core.labels.Badge(field=core.fields.System(name='section-open-in-new-tab-setting')),
            core.labels.Badge(field=core.fields.System(name='section-hide-from-entry-editor-setting')),
            core.labels.Value(field=core.fields.System(name='section-image-id'), value=456),
            core.labels.Empty(field=core.fields.System(name='section-link-out')),
            core.labels.Value(field=core.fields.Custom(name='section-custom-field', path='path.to.field_2'), value='value-1'),
        )),
        core.filters.AnyRange[core.ranges.Range](ranges=(
            core.ranges.Between(field=core.fields.System(name='section-title'), min_value='A', max_value='Z'),
            core.ranges.LessThan(field=core.fields.System(name='section-order-id'), value=30),
        )),
        core.filters.NoRanges[core.ranges.Range](ranges=(
            core.ranges.MoreThan(field=core.fields.System(name='section-order-id'), value=50),
            core.ranges.Between(field=core.fields.Custom(name='section-custom-field', path='path.to.field.3'), min_value=0.01, max_value=0.99),
        )),
    ]
