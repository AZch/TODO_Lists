from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from todo.serializers import TODOSerializer
from users.models import Todotbl, User


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def get_all_todo(request):
    """
    get TODOs
    :param request: data to get
    :return: result get
    """
    TODOs = model_to_dict(Todotbl.objects.all()
                          if request.user.role == User.ADMIN  # role admin
                          else Todotbl.objects.filter(user=request.user))
    return Response(TODOs, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def create_todo(request):
    """
            create TODOs
            :param request: data to create
            :return: result create
            """
    todo = request.data
    todo['user'] = request.user.id
    serializer = TODOSerializer(data=todo)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
