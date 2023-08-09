from rmshared.content.taxonomy import core

Id = core.aliases.system_field('user-id')
Email = core.aliases.system_field('user-email')
Slug = core.aliases.system_field('user-profile-slug')
Title = core.aliases.system_field('user-profile-title')
Owner = core.aliases.system_field('user-profile-owner')
Status = core.aliases.system_field('user-profile-status')
AboutHtml = core.aliases.system_field('user-profile-about-html')
Description = core.aliases.system_field('user-profile-description')
Group = core.aliases.system_field('user-group')
Community = core.aliases.system_field('user-community')
AccessRole = core.aliases.system_field('user-access-role')
LastLoggedInAt = core.aliases.system_field('user-last-logged-in-at')
CustomField = core.aliases.custom_field('user-custom-field')
PostsCount = core.aliases.system_field('user-posts-count')  # TODO: Replace with events/metrics
