from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = User
        fields = ('id', 'email', 'password', 'role',)
        extra_kwargs = {'password': {'write_only': True}}

class TODOSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Todotbl
        fields = ('id', 'name', 'data_task', 'priority', 'user', 'status')