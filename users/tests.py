from django.test import TestCase, Client
from rest_framework import status

from users.models import Todotbl


class User():
    def __init__(self, username, passwrod):
        self.username = username
        self.password = passwrod
        self.nameTODO = 'TODO_Test'
        self.nameTODO_Update = 'TODO_Test_Update'
        self.token = ""

    def login(self):
        client = Client()
        response = client.post('/user/obtain_token/', {'email': self.username, 'passwrod': self.password})
        self.token = response.body["token"]
        return response

    def _create_TODO(self):
        client = Client()
        response = client.post('/user/todo/', {'name': self.nameTODO})
        return response

    def _delete_TDOD(self):
        client = Client()
        response = client.delete('/user/todo/', {'id': Todotbl.objects.get(name=self.nameTODO).id})
        return response

    def _update_TODO(self):
        client = Client()
        client.put('/user/todo/', {'id': Todotbl.objects.get(name=self.nameTODO).id, 'name': self.nameTODO_Update})
        response = client.put('/user/todo/', {'id': Todotbl.objects.get(name=self.nameTODO_Update).id, 'name': self.nameTODO})
        return response

    def _select_TODO(self):
        client = Client()
        response = client.get('/user/todo/')
        return response


class TestUser(TestCase):
    def setUp(self):
        self.admin_user = User('admin@gmail.com', '4628')
        self.noadmin_user = User('noadmin@gmail.com', '4628')

    def test_login_admin(self):
        response = self.admin_user.login()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_noadmin(self):
        response = self.noadmin_user.login()
        self.assertEqual(response.status_code, status.HTTP_200_OK)


