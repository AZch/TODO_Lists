import jwt
from django.conf import settings
from django.contrib.auth import user_logged_in
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.serializers import jwt_payload_handler

from Converts import DBtoObject
from users.serializers import *


class CreateUserAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.query_params
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    # Allow only authenticated users to access this url
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        serializer = self.serializer_class(request.user, data=serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserTaskAPIView(APIView):
    permission_classes = (IsAuthenticated,)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def authenticate_user(request):
    """
    authenticate users with email and password
    :param request: data from page
    :return: result login
    """
    try:
        email = request.query_params['email']
        password = request.query_params['password']

        user = User.objects.get(email=email, password=password)
        if user:
            try:
                payload = jwt_payload_handler(user)
                token = jwt.encode(payload, settings.SECRET_KEY)
                user_details = {}
                user_details['name'] = "%s" % (user.email,)
                user_details['token'] = token
                user_logged_in.send(sender=user.__class__,
                                    request=request, user=user)
                return Response(user_details, status=status.HTTP_200_OK)
            except Exception as e:
                raise e
        else:
            res = {
                'error': 'can not authenticate with the given credentials or the account has been deactivated'
            }
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {
            'error': 'please provide a email or password'
        }
        return Response(res)
