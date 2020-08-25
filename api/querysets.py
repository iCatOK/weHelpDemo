from django.contrib.postgres.search import SearchVector, TrigramSimilarity, SearchRank, SearchQuery
from django.db import models

from api import constants
from functools import reduce


class AbstractQueryset(models.QuerySet):
    search_vector = None
    fields = None
    similarity_to_order_by = constants.DEFAULT_SIMILARITY_SEARCH_ORDER_BY
    vector_order_by = constants.DEFAULT_MODEL_SEARCH_ORDER_BY

    def make_trigram(self, query):
        trigram = 0
        for field in self.fields:
            trigram += TrigramSimilarity(field, query)
        return trigram

    def search(self, query=None):
        qs = self
        if query is not None:
            vector_trigram = self.make_trigram(query=query)
            return qs.annotate(similarity=vector_trigram).\
                filter(similarity__gte=constants.THRESHOLD).\
                order_by(self.similarity_to_order_by) or qs.annotate(search=self.search_vector).\
                order_by(self.vector_order_by).filter(search=query)
        return qs


class UserQueryset(AbstractQueryset):
    search_vector = SearchVector('name', 'surname', 'about_me', 'education_description')
    fields = ['name', 'surname', 'about_me', 'education_description']
    vector_order_by = '-rank'

    def make_search_query(self, query):
        query_words = query.split(' ')
        search_query = reduce(lambda a, b: SearchQuery(a) | SearchQuery(b), query_words)
        return search_query

    def search(self, query=None):
        qs = self
        search_query = self.make_search_query(query)
        search_rank = SearchRank(self.search_vector, search_query)
        if query is not None:
            return qs.annotate(rank=search_rank).\
                order_by(self.vector_order_by).filter(rank__gte=constants.RANK_THRESHOLD)
        return qs


class QuestionQueryset(AbstractQueryset):
    search_vector = SearchVector('name', 'description')
    fields = ['name', 'description']
    vector_order_by = '-pub_date'


class ArticleQueryset(AbstractQueryset):
    search_vector = SearchVector('title', 'content')
    fields = ['title', 'content']
    vector_order_by = '-pub_date'
