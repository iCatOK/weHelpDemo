from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.utils import email_address_exists
from rest_framework import serializers

from api import constants
from api.models import User, Review, Tag, UserTag, Question, Answer, QuestionTag, Article, Comment, ArticleTag
from api.services.serializer_fields import MinimalContentField


def create_tag(request_tag):
    new_tag = Tag.objects.create()
    new_tag.name = request_tag.get('name', new_tag.name)
    new_tag.color = request_tag.get('color', new_tag.color)
    new_tag.save()
    return new_tag


# Serializers define the API representation.

class AnswerIsSolutionSwitchSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())

    class Meta:
        model = Answer
        fields = [
            'id', 'is_solution', 'question'
        ]


class UserThumbnailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'name', 'surname'
        ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color']


# id based
class ReviewSerializer(serializers.ModelSerializer):
    author = UserThumbnailSerializer(read_only=True)
    adressee = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Review
        fields = ['id', 'author', 'adressee', 'text', 'rate', 'pub_date']
        ordering = ['-pub_date']

    def create(self, validated_data):
        review = Review(**validated_data)
        review.author = self.context['request'].user
        review.save()
        return review

    def validate(self, data):
        if data['adressee'] == self.context['request'].user:
            raise serializers.ValidationError("You cannot write review to yourself.")
        if constants.MIN_REVIEW_RATE > data['rate'] > constants.MAX_REVIEW_RATE:
            raise serializers.ValidationError("You can rate only from 1 to 10")
        return data


class AnswerSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    author = UserThumbnailSerializer(read_only=True)

    # TODO: убрать это, сделав пользователя по умолчанию
    def create(self, validated_data):
        answer = Answer(**validated_data)
        answer.author = self.context['request'].user
        answer.save()
        return answer

    class Meta:
        model = Answer
        ordering = ['-pub_date']
        fields = [
            'id', 'text', 'rating',
            'is_solution', 'author',
            'pub_date', 'question'
        ]
        extra_kwargs = {
            'author': {'read_only': True},
            'rating': {'read_only': True},
            'question': {'read_only': True},
            'is_solution': {'read_only': True},
        }


class CommentSerializer(serializers.ModelSerializer):
    article = serializers.PrimaryKeyRelatedField(queryset=Article.objects.all())
    author = UserThumbnailSerializer(read_only=True)

    # TODO: убрать это, сделав пользователя по умолчанию
    def create(self, validated_data):
        comment = Comment(**validated_data)
        comment.author = self.context['request'].user
        comment.save()
        return comment

    class Meta:
        model = Comment
        ordering = ['-pub_date']
        fields = [
            'id', 'content',
            'author', 'pub_date', 'article'
        ]
        extra_kwargs = {
            'author': {'read_only': True},
            'article': {'read_only': True},
        }


class ArticleDetailSerializer(serializers.ModelSerializer):
    author = UserThumbnailSerializer(read_only=True)
    tags = TagSerializer(many=True)
    comments = CommentSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()

        article_tags = validated_data.get('tags')

        for request_tag in article_tags:
            tag_name = request_tag.get('name')
            if not Tag.objects.filter(name=tag_name).exists():
                tag = create_tag(request_tag)
            else:
                tag = Tag.objects.filter(name=tag_name)[0]
            if not ArticleTag.objects.filter(article=instance, tag=tag).exists():
                at = ArticleTag.objects.create(
                    article=instance,
                    tag=tag,
                )
                at.save()

        return instance

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'content',
            'author', 'tags',
            'pub_date', 'comments', 'comment_count'
        ]
        extra_kwargs = {
            'author': {'read_only': True},
            'comments': {'read_only': True},
            'comment_count': {'read_only': True}
        }


class QuestionDetailSerializer(serializers.ModelSerializer):
    author = UserThumbnailSerializer(read_only=True)
    tags = TagSerializer(many=True)
    answers = AnswerSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        question_tags = validated_data.get('tags')

        for request_tag in question_tags:
            tag = Tag
            tag_name = request_tag.get('name')
            if not Tag.objects.filter(name=tag_name).exists():
                tag = create_tag(request_tag)
            else:
                tag = Tag.objects.filter(name=tag_name)[0]
            if not QuestionTag.objects.filter(question=instance, tag=tag).exists():
                qt = QuestionTag.objects.create(
                    question=instance,
                    tag=tag,
                )
                qt.save()

        return instance

    class Meta:
        model = Question
        fields = [
            'id', 'name', 'description',
            'author', 'tags',
            'pub_date', 'answers', 'answer_count'
        ]
        extra_kwargs = {
            'author': {'read_only': True},
            'answers': {'read_only': True},
            'answer_count': {'read_only': True}
        }


class QuestionListSerializer(serializers.ModelSerializer):
    author = UserThumbnailSerializer(read_only=True)
    tags = TagSerializer(many=True)

    def create(self, validated_data):
        question_tags = validated_data.pop('tags', None)
        question = Question(**validated_data)
        question.author = self.context['request'].user
        question.save()

        for request_tag in question_tags:
            tag_name = request_tag.get('name')
            if not Tag.objects.filter(name=tag_name).exists():
                tag = create_tag(request_tag)
            else:
                tag = Tag.objects.filter(name=tag_name)[0]
            qt = QuestionTag.objects.create(
                question=question,
                tag=tag,
            )
            qt.save()

        question.save()
        return question

    class Meta:
        model = Question
        fields = [
            'id', 'name', 'description',
            'author', 'tags', 'answer_count',
            'pub_date'
        ]
        extra_kwargs = {
            'author': {'read_only': True},
            'answer_count': {'read_only': True}
        }
        ordering = ['-pub_date']


class ArticleListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    content = MinimalContentField()

    def create(self, validated_data):
        article_tags = validated_data.pop('tags', None)
        article = Article(**validated_data)
        article.author = self.context['request'].user
        article.save()

        for request_tag in article_tags:
            tag_name = request_tag.get('name')
            if not Tag.objects.filter(name=tag_name).exists():
                tag = create_tag(request_tag)
            else:
                tag = Tag.objects.filter(name=tag_name)[0]
            at = ArticleTag.objects.create(
                article=article,
                tag=tag,
            )
            at.save()

        article.save()
        return article

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'content',
            'tags', 'comment_count',
            'pub_date'
        ]
        extra_kwargs = {
            'comment_count': {'read_only': True}
        }
        ordering = ['-pub_date']


# id based user detail

class UserDetailSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    articles = ArticleListSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'name', 'surname',
            'about_me', 'education_description', 'tags',
            'rating', 'reviews', 'articles', 'answer_count',
            'question_count'
        ]
        extra_kwargs = {
            'rating': {'read_only': True},
            'answer_count':  {'read_only': True},
            'question_count':  {'read_only': True},
            'name': {'read_only': True},
            'surname':  {'read_only': True},
            'about_me':  {'read_only': True},
            'education_description': {'read_only': True},
        }


class AccountDetailSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True)
    articles = ArticleListSerializer(many=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'phone', 'name', 'surname',
            'about_me', 'education_description', 'tags',
            'rating', 'reviews', 'articles', 'answer_count',
            'question_count'
        ]

        extra_kwargs = {
            'rating': {'read_only': True},
            'phone_number': {'read_only': False},
            'reviews': {'read_only': True},
            'articles':  {'read_only': True},
            'answer_count':  {'read_only': True},
            'question_count':  {'read_only': True},
        }

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.surname = validated_data.get('surname', instance.surname)
        instance.about_me = validated_data.get('about_me', instance.about_me)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.education_description = validated_data.get('education_description', instance.education_description)
        instance.save()

        user_tags = validated_data.get('tags')

        for request_tag in user_tags:
            tag_name = request_tag.get('name')
            if not Tag.objects.filter(name=tag_name).exists():
                tag = create_tag(request_tag)
            else:
                tag = Tag.objects.filter(name=tag_name)[0]
            if not UserTag.objects.filter(user=instance, tag=tag).exists():
                ut = UserTag.objects.create(
                    user=instance,
                    tag=tag,
                )
                ut.save()

        return instance


# id based userList
# swagger - userMinimum

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'surname', 'rating']
        extra_kwargs = {
            'rating': {'read_only': True},
            'id': {'read_only': True},
            'name': {'read_only': True},
            'surname': {'read_only': True}
        }


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    name = serializers.CharField(required=True, write_only=True)
    surname = serializers.CharField(required=True, write_only=True)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    ("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(
                ("The two password fields didn't match."))
        return data

    def get_cleaned_data(self):
        return {
            'name': self.validated_data.get('name', ''),
            'surname': self.validated_data.get('surname', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])

        user.save()
        return user


from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext as _

from allauth.socialaccount.models import SocialLogin
from dj_rest_auth.registration.serializers import SocialLoginSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class CallbackSerializer(SocialLoginSerializer):
    state = serializers.CharField()

    def validate_state(self, value):
        """
        Checks that the state is equal to the one stored in the session.
        """
        try:
            SocialLogin.verify_and_unstash_state(
                self.context['request'],
                value,
            )
        # Allauth raises PermissionDenied if the validation fails
        except PermissionDenied:
            raise ValidationError(_('State did not match.'))
        return value
