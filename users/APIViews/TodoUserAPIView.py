from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from Converts import DBtoObject
from WordConst import Roles
from users.serializers import TODOSerializer, Todotbl


class TodoUserAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        todo = dict(request.query_params)
        todo['name'] = ''.join(todo['name'])
        todo['user'] = request.user.id
        serializer = TODOSerializer(data=todo)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        TODOs = DBtoObject.dictTODOs(Todotbl.objects.all()
                                     if request.user.role == Roles.admin
                                     else Todotbl.objects.filter(user=request.user))
        return Response(TODOs, status=status.HTTP_200_OK)

    def put(self, request):
        Todotbl.objects.filter(id=request.data['id']).update(
            user=request.data['user']['id'],
            name=request.data['name'],
            data_task=request.data['data_task'],
            status=request.data['status'],
            priority=request.data['priority']
        )
        return Response(DBtoObject.dictTODO(Todotbl.objects.get(id=request.data["id"])), status=status.HTTP_200_OK)

    def delete(self, request):
        todo = Todotbl.objects.filter(id=request.data['id'])
        if todo:
            todo.delete()
            res = {'res': 'complete delete'}
        else:
            res = {'res': 'cant find TODO'}
        return Response(res, status=status.HTTP_200_OK)