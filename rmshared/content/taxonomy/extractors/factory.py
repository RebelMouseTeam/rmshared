from rmshared.content.taxonomy import graph

from rmshared.content.taxonomy.extractors.abc import IValuesExtractor
from rmshared.content.taxonomy.extractors.values import PostValuesExtractor


class Factory:
    @staticmethod
    def make_extractor_for_post(post: graph.posts.Post) -> IValuesExtractor:
        return PostValuesExtractor(post)
