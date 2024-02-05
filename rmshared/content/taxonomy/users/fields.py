from rmshared.content.taxonomy import core

Id = core.aliases.fields.System('user-id')
Email = core.aliases.fields.System('user-email')
Slug = core.aliases.fields.System('user-profile-slug')
Title = core.aliases.fields.System('user-profile-title')
Owner = core.aliases.fields.System('user-profile-owner')
Status = core.aliases.fields.System('user-profile-status')
CreatedAt = core.aliases.fields.System('user-profile-created-at')
AboutHtml = core.aliases.fields.System('user-profile-about-html')
Description = core.aliases.fields.System('user-profile-description')
Group = core.aliases.fields.System('user-group')
Community = core.aliases.fields.System('user-community')
AccessRole = core.aliases.fields.System('user-access-role')
LastLoggedInAt = core.aliases.fields.System('user-last-logged-in-at')
CustomField = core.aliases.fields.Custom('user-custom-field')
PostsCount = core.aliases.fields.System('user-posts-count')  # TODO: Replace with events/metrics
