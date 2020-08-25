from django.contrib.postgres.indexes import GinIndex
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager

from api import managers
from api.managers import UserManager


class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        null=False,
        blank=False
    )
    color = models.CharField(
        max_length=25,
        null=False,
        blank=False
    )


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)

    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)

    phone = models.CharField(null=True, blank=True, max_length=11)

    about_me = models.CharField(
        max_length=600,
        null=True,
        blank=True
    )

    education_description = models.CharField(
        max_length=600,
        null=True,
        blank=True
    )

    rating = models.FloatField(
        default=0.0,
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    tags = models.ManyToManyField(Tag, through="UserTag")

    answer_count = models.IntegerField(default=0)
    question_count = models.IntegerField(default=0)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        indexes = [GinIndex(fields=['email'])]

    def __str__(self):
        return self.email

    def __unicode__(self):
        return self.email

    def get_short_name(self):
        return self.email

    def get_full_name(self):
        return '%s %s' % (self.name, self.surname)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def recount_answer_count(self):
        self.answer_count = self.answers.count()
        self.save()

    def recount_question_count(self):
        self.question_count = self.questions.count()
        self.save()

    def recount_rating(self):
        if self.reviews.count() == 0:
            self.rating = 0
            self.save()

        new_rating = 0.0
        for review in self.reviews.all():
            new_rating += review.rate
        self.rating = new_rating / self.reviews.count()
        self.save()


class Review(models.Model):
    text = models.CharField(
        max_length=600,
        blank=True,
        default=""
    )

    rate = models.IntegerField(default=10)

    pub_date = models.DateField(auto_now=True)
    author = models.ForeignKey('api.User', on_delete=models.CASCADE)
    adressee = models.ForeignKey('api.User', on_delete=models.CASCADE, related_name="reviews")

    class Meta:
        ordering = ['-pub_date']


class Question(models.Model):
    name = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )
    description = models.CharField(
        max_length=300,
        null=False,
        blank=False
    )
    pub_date = models.DateField(auto_now=True)
    author = models.ForeignKey('api.User', on_delete=models.CASCADE, related_name="questions")
    tags = models.ManyToManyField(Tag, through="QuestionTag")
    answer_count = models.IntegerField(default=0)
    objects = managers.QuestionManager()

    def recount_answer_count(self):
        self.answer_count = self.answers.count()
        self.save()

    class Meta:
        ordering = ['-pub_date']
        indexes = [GinIndex(fields=['name'])]


class Answer(models.Model):
    text = models.CharField(
        max_length=600,
        null=False,
        blank=False
    )

    pub_date = models.DateField(auto_now=True)
    rating = models.IntegerField(default=0)
    is_solution = models.BooleanField(default=False)
    author = models.ForeignKey('api.User', on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey('api.Question', on_delete=models.CASCADE, related_name="answers")

    class Meta:
        ordering = ['-pub_date']


class Article(models.Model):
    title = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )
    content = models.CharField(
        max_length=2000,
        null=False,
        blank=False
    )
    pub_date = models.DateField(auto_now=True)
    author = models.ForeignKey('api.User', on_delete=models.CASCADE, related_name="articles")
    tags = models.ManyToManyField(Tag, through="ArticleTag")
    comment_count = models.IntegerField(default=0)
    objects = managers.ArticleManager()

    def recount_comment_count(self):
        self.comment_count = self.comments.count()
        self.save()

    class Meta:
        ordering = ['-pub_date']
        indexes = [GinIndex(fields=['title'])]


class Comment(models.Model):
    author = models.ForeignKey('api.User', on_delete=models.CASCADE)
    article = models.ForeignKey('api.Article', on_delete=models.CASCADE, related_name="comments")
    pub_date = models.DateField(auto_now=True)
    content = models.CharField(
        max_length=300,
        null=False,
        blank=False
    )

    class Meta:
        ordering = ['-pub_date']


class UserTag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class QuestionTag(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class ArticleTag(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


