from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = User
        fields = ('id', 'email', 'password', 'role',)
        extra_kwargs = {'password': {'write_only': True}}