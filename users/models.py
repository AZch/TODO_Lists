from __future__ import unicode_literals

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
from django.db import models, transaction

from WordConst import Roles


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields('role', Roles.admin)
        return self._create_user(email, password=password, **extra_fields)

class TodoManager(models.Manager):
    def _create_todo(self, name, userid, **extra_fields):
        if not name:
            raise ValueError('Name must be set')
        try:
            with transaction.atomic():
                todo = self.model(name=name, userid=userid, **extra_fields)
                todo.save(using=self.__db)
                return todo
        except:
            raise

    def create_todo(self, name, userid, **extra_fields):
        return self._create_todo(name, userid, **extra_fields)

class User(AbstractBaseUser):
    email = models.EmailField(max_length=40, unique=True)
    role = models.CharField(max_length=50, default='')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self

class Todotbl(models.Model):
    idtodo = models.IntegerField(auto_created=True, unique=True)
    name = models.CharField(max_length=100)
    data = models.CharField(max_length=1000, default='')
    property = models.IntegerField(default=0)
    userid = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    object = TodoManager()

    REQUIRED_FIELDS = ['name', 'userid', 'idtodo']

