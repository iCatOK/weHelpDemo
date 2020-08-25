from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from api import search_views
from api.views import TagList, TagDetail, QuestionList, QuestionDetail, AnswerList, AnswerDetail, \
    AnswerIsSolutionSwitchView, ArticleList, ArticleDetail, CommentList, CommentDetail
from .views import UserList, UserDetail, ReviewList, ReviewDetail

router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)
#router.register(r'reviews', views.ReviewViewSet)

user_list = UserList.as_view()
user_detail = UserDetail.as_view()
user_search = search_views.UserSearchView.as_view()

review_list = ReviewList.as_view()
review_detail = ReviewDetail.as_view()

app_name = 'api'

review_patterns = [
    path('', review_list, name='review-list'),
    path('<int:pk>/', review_detail, name='review-detail'),
]

question_patterns = [
    path('', QuestionList.as_view(), name='question-list'),
    path('search/', search_views.QuestionSearchView.as_view(), name='question-search'),
    path('<int:pk>/', QuestionDetail.as_view(), name='question-detail'),
]

article_patterns = [
    path('', ArticleList.as_view(), name='article-list'),
    path('search/', search_views.ArticleSearchView.as_view(), name='article-search'),
    path('<int:pk>/', ArticleDetail.as_view(), name='article-detail'),
]

answer_patterns = [
    path('', AnswerList.as_view(), name='answer-list'),
    path('<int:pk>/', AnswerDetail.as_view(), name='answer-detail'),
    path('<int:pk>/solution/', AnswerIsSolutionSwitchView.as_view(), name='answer-switch-solution-view')
]

comment_patterns = [
    path('', CommentList.as_view(), name='comment-list'),
    path('<int:pk>/', CommentDetail.as_view(), name='comment-detail'),
]

tag_patterns = [
    path('', TagList.as_view(), name='tag-list'),
    path('<int:pk>/', TagDetail.as_view(), name='tag-detail'),
]


urlpatterns = [
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail'),
    path('users/search/', user_search, name='user-search'),
    path('reviews/', include(review_patterns)),
    path('tags/', include(tag_patterns)),
    path('questions/', include(question_patterns)),
    path('answers/', include(answer_patterns)),
    path('articles/', include(article_patterns)),
    path('comments/', include(comment_patterns)),
]