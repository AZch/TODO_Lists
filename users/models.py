from __future__ import unicode_literals

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models, transaction


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
        extra_fields('role', User.ADMIN)
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


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=40, unique=True)

    ADMIN = 'ADMIN'
    NOADMIN = 'NOADMIN'

    ROLE_CHOICE = [
        (ADMIN, 'admin'),
        (NOADMIN, 'no admin')
    ]

    role = models.CharField(max_length=50,
                            choices=ROLE_CHOICE,
                            default=NOADMIN)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self


class Todotbl(models.Model):
    name = models.CharField(max_length=100)
    data_task = models.CharField(max_length=1000, default='', blank=True)
    priority = models.IntegerField(default=0)
    NEW = 'NEW'
    START = 'START'
    WORK = 'WORK'
    PAUSE = 'PAUSE'
    END = 'END'
    STATUS_CHOICES = [
        (NEW, 'new'),
        (START, 'start'),
        (WORK, 'work'),
        (PAUSE, 'pause'),
        (END, 'end')
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=NEW
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    objects = TodoManager()

    REQUIRED_FIELDS = ['name', 'status']
