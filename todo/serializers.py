from rest_framework import serializers

from users.models import *


class TODOSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Todotbl
        fields = ('id', 'name', 'data_task', 'priority', 'user', 'status')
