from django.contrib.auth.base_user import BaseUserManager
from django.db import models

from api.querysets import UserQueryset, QuestionQueryset, ArticleQueryset


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Staff must have is_staff=True')

        return self._create_user(email, password, **extra_fields)

    def get_queryset(self):
        return UserQueryset(self.model, using=self._db)


class QuestionManager(models.Manager):
    def get_queryset(self):
        return QuestionQueryset(self.model, using=self._db)


class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQueryset(self.model, using=self._db)

