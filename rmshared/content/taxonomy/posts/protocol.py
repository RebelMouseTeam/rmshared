from typing import Any
from typing import Callable
from typing import Mapping
from typing import Type
from typing import TypeVar

from rmshared.tools import invert_dict
from rmshared.tools import parse_name_and_info
from rmshared.tools import ensure_map_is_complete

from rmshared.content.taxonomy.posts import consts
from rmshared.content.taxonomy.posts import drafts
from rmshared.content.taxonomy.posts import statuses
from rmshared.content.taxonomy.posts import published
from rmshared.content.taxonomy.posts.abc import IProtocol

Status = TypeVar('Status', bound=statuses.Status)
Stage = TypeVar('Stage', bound=drafts.stages.Stage)
Scope = TypeVar('Scope', bound=published.scopes.Scope)


class Protocol(IProtocol):
    def __init__(self):
        self.post_status_to_id_map: Mapping[Type[Status], str] = ensure_map_is_complete(statuses.Status, {
            statuses.Draft: 'draft',
            statuses.Published: 'published',
            statuses.Removed: 'removed',
        })
        self.post_status_from_id_map: Mapping[str, Type[Status]] = invert_dict(self.post_status_to_id_map)
        self.post_status_to_make_func_map: Mapping[Type[Status], Callable[[Mapping[str, Any]], Status]] = ensure_map_is_complete(statuses.Status, {
            statuses.Draft: self._make_draft_post_status,
            statuses.Published: self._make_published_post_status,
            statuses.Removed: lambda _: statuses.Removed(),
        })
        self.post_status_to_jsonify_info_func_map = ensure_map_is_complete(statuses.Status, {
            statuses.Draft: self._jsonify_draft_status_info,
            statuses.Published: self._jsonify_published_status_info,
            statuses.Removed: lambda _: {},
        })
        self.draft_stage_to_id_map: Mapping[Type[drafts.stages.Stage], str] = ensure_map_is_complete(drafts.stages.Stage, {
            drafts.stages.Created: 'created',
            drafts.stages.InProgress: 'in-progress',
            drafts.stages.InReview: 'in-review',
            drafts.stages.Ready: 'ready',
        })
        self.draft_stage_from_id_map: Mapping[str, Type[drafts.stages.Stage]] = invert_dict(self.draft_stage_to_id_map)
        self.draft_stage_to_make_func_map: Mapping[Type[Stage], Callable[[Mapping[str, Any]], Stage]] = ensure_map_is_complete(drafts.stages.Stage, {
            drafts.stages.Created: self._make_created_draft_stage,
            drafts.stages.InProgress: self._make_in_progress_draft_stage,
            drafts.stages.InReview: lambda _: drafts.stages.InReview(),
            drafts.stages.Ready: lambda _: drafts.stages.Ready(),
        })
        self.draft_stage_to_jsonify_info_func_map: Mapping[Type[Stage], Callable[[Stage], Mapping[str, Any]]] = ensure_map_is_complete(drafts.stages.Stage, {
            drafts.stages.Created: self._jsonify_created_draft_stage_info,
            drafts.stages.InProgress: self._jsonify_in_progress_draft_stage_info,
            drafts.stages.InReview: lambda _: {},
            drafts.stages.Ready: lambda _: {},
        })
        self.published_scope_to_id_map: Mapping[Type[published.scopes.Scope], str] = ensure_map_is_complete(published.scopes.Scope, {
            published.scopes.Site: 'site',
            published.scopes.Community: 'community',
        })
        self.published_scope_from_id_map: Mapping[str, Type[published.scopes.Scope]] = invert_dict(self.published_scope_to_id_map)
        self.published_scope_to_make_func_map: Mapping[Type[Scope], Callable[[Mapping], Scope]] = ensure_map_is_complete(published.scopes.Scope, {
            published.scopes.Site: self._make_site_published_scope,
            published.scopes.Community: self._make_community_published_scope,
        })
        self.published_scope_to_jsonify_info_func_map: Mapping[Type[Scope], Callable[[Scope], Mapping]] = ensure_map_is_complete(published.scopes.Scope, {
            published.scopes.Site: self._jsonify_site_published_scope_info,
            published.scopes.Community: self._jsonify_community_published_scope_info,
        })

    def make_post_type(self, data):
        name, info = parse_name_and_info(data)
        assert info == {}
        return self.POST_TYPE_FROM_ID_MAP[name]

    def jsonify_post_type(self, post_type):
        return {self.POST_TYPE_TO_ID_MAP[post_type]: {}}

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
    POST_TYPE_FROM_ID_MAP = invert_dict(POST_TYPE_TO_ID_MAP)
    assert frozenset(POST_TYPE_FROM_ID_MAP.values()) == consts.POST.TYPE.ALL

    def make_post_status(self, data):
        name, info = parse_name_and_info(data)
        return self.post_status_to_make_func_map[self.post_status_from_id_map[name]](dict(info))

    def jsonify_post_status(self, status):
        name = self.post_status_to_id_map[type(status)]
        info = self.post_status_to_jsonify_info_func_map[type(status)](status)
        return {name: info}

    def _make_draft_post_status(self, info: Mapping[str, Any]) -> statuses.Draft:
        return statuses.Draft(stage=self._make_draft_stage(info['stage']))

    def _jsonify_draft_status_info(self, status: statuses.Draft) -> Mapping[str, Any]:
        return {'stage': self._jsonify_draft_stage(status.stage)}

    def _make_draft_stage(self, info: Mapping[str, Any]) -> drafts.stages.Stage:
        name, info = parse_name_and_info(info)
        return self.draft_stage_to_make_func_map[self.draft_stage_from_id_map[name]](dict(info))

    def _jsonify_draft_stage(self, stage: drafts.stages.Stage) -> Mapping[str, Any]:
        name = self.draft_stage_to_id_map[type(stage)]
        info = self.draft_stage_to_jsonify_info_func_map[type(stage)](stage)
        return {name: info}

    @staticmethod
    def _make_created_draft_stage(info: Mapping[str, Any]) -> drafts.stages.Created:
        return drafts.stages.Created(is_imported=bool(info['is_imported']))

    @staticmethod
    def _jsonify_created_draft_stage_info(stage: drafts.stages.Created) -> Mapping[str, Any]:
        return {'is_imported': stage.is_imported}

    @staticmethod
    def _make_in_progress_draft_stage(info: Mapping[str, Any]) -> drafts.stages.InProgress:
        return drafts.stages.InProgress(is_rejected=bool(info['is_rejected']))

    @staticmethod
    def _jsonify_in_progress_draft_stage_info(stage: drafts.stages.InProgress) -> Mapping[str, Any]:
        return {'is_rejected': stage.is_rejected}

    def _make_published_post_status(self, info: Mapping[str, Any]) -> statuses.Published:
        return statuses.Published(scope=self._make_published_scope(dict(info['scope'])))

    def _jsonify_published_status_info(self, status: statuses.Published) -> Mapping[str, Any]:
        return {'scope': self._jsonify_published_scope(status.scope)}

    def _make_published_scope(self, info: Mapping[str, Any]) -> published.scopes.Scope:
        name, info = parse_name_and_info(info)
        return self.published_scope_to_make_func_map[self.published_scope_from_id_map[name]](dict(info))

    def _jsonify_published_scope(self, scope: published.scopes.Scope) -> Mapping[str, Any]:
        name = self.published_scope_to_id_map[type(scope)]
        info = self.published_scope_to_jsonify_info_func_map[type(scope)](scope)
        return {name: info}

    @staticmethod
    def _make_site_published_scope(info: Mapping[str, Any]) -> published.scopes.Site:
        return published.scopes.Site(is_promoted=bool(info['is_promoted']))

    @staticmethod
    def _jsonify_site_published_scope_info(scope: published.scopes.Site) -> Mapping[str, Any]:
        return {'is_promoted': scope.is_promoted}

    @staticmethod
    def _make_community_published_scope(info: Mapping[str, Any]) -> published.scopes.Community:
        return published.scopes.Community(is_demoted=bool(info['is_demoted']))

    @staticmethod
    def _jsonify_community_published_scope_info(scope: published.scopes.Community) -> Mapping[str, Any]:
        return {'is_demoted': scope.is_demoted}
