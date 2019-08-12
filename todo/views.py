from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Converts import DBtoObject
from users.models import Todotbl, User


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def get_all_todo(request):
    """
    get TODOs
    :param request: data to get
    :return: result get
    """
    TODOs = DBtoObject.dictTODOs(Todotbl.objects.all()
                                 if request.user.role == User.ROLE_CHOICE[0][0]  # role admin
                                 else Todotbl.objects.filter(user=request.user))
    return Response(TODOs, status=status.HTTP_200_OK)