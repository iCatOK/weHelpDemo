from rest_framework import permissions
from rest_framework import serializers, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api import permissions as api_permissions
from api import serializers
from api.models import User, Review, Tag, Question, Answer, Article, Comment
from api.serializers import AnswerIsSolutionSwitchSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserListSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserDetailSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, 
        api_permissions.IsItselfOrReadOnly
    ]


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, 
    ]


class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = serializers.QuestionDetailSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        api_permissions.IsAuthorOrReadOnly
    ]


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = serializers.ArticleDetailSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        api_permissions.IsAuthorOrReadOnly
    ]


class QuestionList(generics.ListCreateAPIView):
    serializer_class = serializers.QuestionListSerializer
    queryset = Question.objects.all()
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]


class ArticleList(generics.ListCreateAPIView):
    serializer_class = serializers.ArticleListSerializer
    queryset = Article.objects.all()
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]


class AnswerList(generics.ListCreateAPIView):
    serializer_class = serializers.AnswerSerializer
    queryset = Answer.objects.all()
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]


class CommentList(generics.ListCreateAPIView):
    serializer_class = serializers.CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]


class AnswerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = serializers.AnswerSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        api_permissions.IsAuthorOrReadOnly,
    ]


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        api_permissions.IsAuthorOrReadOnly,
    ]


class AnswerIsSolutionSwitchView(generics.UpdateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerIsSolutionSwitchSerializer
    permission_classes = [
        api_permissions.IsAuthorOfQuestionOrReadOnly
    ]


class ReviewList(generics.ListCreateAPIView):
    serializer_class = serializers.ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]


class TagList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


@api_view(['POST', ])
def registration_view(request):
    serializer = serializers.RegisterSerializer(data=request.data)
    data = {}

    if serializer.is_valid():
        user = serializer.save(request)
        data['response'] = 'Registration Succsseed!'
        data['email'] = user.email
        data['name'] = user.name
        data['surname'] = user.surname
    else:
        data = serializer.errors
    
    return Response(data)