from rmshared.content.taxonomy import core

Id = core.aliases.fields.System('section-id')
Path = core.aliases.fields.System('section-path')
Slug = core.aliases.fields.System('section-slug')
Title = core.aliases.fields.System('section-title')
OrderId = core.aliases.fields.System('section-order-id')
CreatedAt = core.aliases.fields.System('section-profile-created-at')
IsReadOnly = core.aliases.fields.System('section-is-read-only')

ParentId = core.aliases.fields.System('section-parent-id')
# TODO: consider `ParentSlug = core.aliases.fields.System('section-parent-slug')`
AncestorId = core.aliases.fields.System('section-ancestor-id')
# TODO: consider `AncestorSlug = core.aliases.fields.System('section-ancestor-slug')`

Visibility = core.aliases.fields.System('section-visibility')
ReadAccess = core.aliases.fields.System('section-read-access-kind')

OpenInNewTabSetting = core.aliases.fields.System('section-open-in-new-tab-setting')
AllowCommunityPostsSetting = core.aliases.fields.System('section-allow-community-posts-setting')
HideFromEntryEditorSetting = core.aliases.fields.System('section-hide-from-entry-editor-setting')
LockPostsAfterPublishingSetting = core.aliases.fields.System('section-lock-posts-after-publishing-setting')

ImageId = core.aliases.fields.System('section-image-id')
LinkOut = core.aliases.fields.System('section-link-out')
MetaTag = core.aliases.fields.System('section-meta-tag')
MetaTitle = core.aliases.fields.System('section-meta-title')
AboutHtml = core.aliases.fields.System('section-about-html')

CustomField = core.aliases.fields.Custom('section-custom-field')
# TODO: PostsCount = core.aliases.fields.System('section-posts-count')  # TODO: Replace with events/metrics
