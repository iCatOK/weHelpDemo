from rest_framework.response import Response
from rest_framework.views import APIView

from api.services import search


class QuestionSearchView(APIView):
    def get(self, request, format=None):
        return Response(search.get_questions(request.data['query']))


class UserSearchView(APIView):
    def get(self, request, format=None):
        return Response(search.get_users(request.data['query']))


class ArticleSearchView(APIView):
    def get(self, request, format=None):
        return Response(search.get_articles(request.data['query']))
