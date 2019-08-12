from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import Todotbl


class TodoUserAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def test_access(self, id_user, id_todo):
        user = User.objects.get(id=id_user)
        if user.role == User.ADMIN:
            return True
        else:
            try:
                Todotbl.objects.get(id=id_todo, user_id=id_user)
                return True
            except:
                return False

    def get(self, request, id):
        """
        get TODOs
        :param id: id todos
        :param request: data to get
        :return: result get
        """

        if self.test_access(request.user.id, id):
            try:
                todo = Todotbl.objects.get(id=id)
                return Response(model_to_dict(todo), status=status.HTTP_200_OK)
            except:
                res = {
                    'error': 'please provide id todo'
                }
                return Response(res)
        else:
            res = {
                'error': 'please access or provide to this id todo'
            }
            return Response(res)

    def put(self, request, id):
        """
        edit TODOs
        :param id: id todos
        :param request: data to edit
        :return: result edit
        """
        if self.test_access(request.user.id, id):
            try:
                Todotbl.objects.filter(id=id).update(
                    user=request.data['user']['id'],
                    name=request.data['name'],
                    data_task=request.data['data_task'],
                    status=request.data['status'],
                    priority=request.data['priority']
                )
                return Response(model_to_dict(Todotbl.objects.get(id=id)), status=status.HTTP_200_OK)
            except:
                res = {
                    'error': 'please provide id todo'
                }
                return Response(res)
        else:
            res = {
                'error': 'please access or provide to this id todo'
            }
            return Response(res)

    def delete(self, request, id):
        """
        remove TODOs
        :param id: id todos
        :param request: data to remove
        :return: result remove
        """
        if self.test_access(request.user.id, id):
            try:
                Todotbl.objects.filter(id=id).delete()
                res = {'res': 'complete delete'}
                return Response(res, status=status.HTTP_200_OK)
            except:
                res = {
                    'error': 'please provide id todo'
                }
                return Response(res)
        else:
            res = {
                'error': 'please access or provide to this id todo'
            }
            return Response(res)
