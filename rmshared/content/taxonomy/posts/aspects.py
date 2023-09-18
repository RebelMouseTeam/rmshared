from typing import Callable
from typing import Mapping
from typing import Type
from typing import TypeVar

from rmshared.tools import ensure_map_is_complete

from rmshared.content.taxonomy.posts import consts
from rmshared.content.taxonomy.posts import statuses
from rmshared.content.taxonomy.posts import drafts
from rmshared.content.taxonomy.posts import published
from rmshared.content.taxonomy.posts.abc import IAspects

Status = TypeVar('Status', bound=statuses.Status)
Stage = TypeVar('Stage', bound=drafts.stages.Stage)
Scope = TypeVar('Scope', bound=published.scopes.Scope)


class Aspects(IAspects):
    def __init__(self):
        self.post_status_to_factory_func_map: Mapping[Type[Status], Callable[[Status], str]] = ensure_map_is_complete(statuses.Status, {
            statuses.Draft: self._map_draft_post_status,
            statuses.Published: self._map_published_post_status,
            statuses.Removed: lambda _: 'removed',
        })
        self.draft_post_stage_to_factory_func_map: Mapping[Type[Stage], Callable[[Stage], str]] = ensure_map_is_complete(drafts.stages.Stage, {
            drafts.stages.Created: self._map_draft_post_created_stage,
            drafts.stages.InProgress: self._map_draft_post_in_progress_stage,
            drafts.stages.InReview: lambda _: 'in-review',
            drafts.stages.Ready: lambda _: 'ready',
        })
        self.published_post_scope_to_factory_func_map: Mapping[Type[Scope], Callable[[Scope], str]] = ensure_map_is_complete(published.scopes.Scope, {
            published.scopes.Site: self._map_published_post_site_scope,
            published.scopes.Community: self._map_published_post_community_scope,
        })

    def map_post_type(self, type_):
        return self.POST_TYPE_TO_ID_MAP[type_]

    POST_TYPE_TO_ID_MAP = {
        consts.POST.TYPE.PAGE: 'page',
        consts.POST.TYPE.IMAGE: 'image',
        consts.POST.TYPE.VIDEO: 'video',
        consts.POST.TYPE.EVENT: 'event',
        consts.POST.TYPE.PLACE: 'place',
        consts.POST.TYPE.HOW_TO: 'how-to',
        consts.POST.TYPE.RECIPE: 'recipe',
        consts.POST.TYPE.PRODUCT: 'product',
    }
    assert set(POST_TYPE_TO_ID_MAP.keys()) == consts.POST.TYPE.ALL

    def map_post_status(self, status):
        return self.post_status_to_factory_func_map[type(status)](status)

    def _map_draft_post_status(self, status: statuses.Draft) -> str:
        return f'draft-{self._map_draft_post_stage(status.stage)}'

    def _map_draft_post_stage(self, stage: drafts.stages.Stage) -> str:
        return self.draft_post_stage_to_factory_func_map[type(stage)](stage)

    @staticmethod
    def _map_draft_post_created_stage(stage: drafts.stages.Created) -> str:
        return f'created(imported={str(stage.is_imported).lower()})'

    @staticmethod
    def _map_draft_post_in_progress_stage(stage: drafts.stages.InProgress) -> str:
        return f'in-progress(rejected={str(stage.is_rejected).lower()})'

    def _map_published_post_status(self, status: statuses.Published) -> str:
        return f'published-to-{self._map_published_post_scope(status.scope)}'

    def _map_published_post_scope(self, scope: published.scopes.Scope) -> str:
        return self.published_post_scope_to_factory_func_map[type(scope)](scope)

    @staticmethod
    def _map_published_post_site_scope(scope: published.scopes.Site) -> str:
        return f'site(promoted={str(scope.is_promoted).lower()})'

    @staticmethod
    def _map_published_post_community_scope(scope: published.scopes.Community) -> str:
        return f'community(demoted={str(scope.is_demoted).lower()})'
