from django.conf.urls import url

from users.APIViews.CreateUserAPIView import CreateUserAPIView
from users.APIViews.FilterTaskAPIView import FilterTaskAPIView
from users.APIViews.TodoUserAPIView import TodoUserAPIView
from users.APIViews.UserRetrieveUpdateAPIView import UserRetrieveUpdateAPIView
from .views import *

app_name = 'users'

urlpatterns = [
    url(r'^create/$', CreateUserAPIView.as_view()),
    url(r'^test_token', authenticate_user),
    url(r'^update/$', UserRetrieveUpdateAPIView.as_view()),
    url(r'^task/$', TodoUserAPIView.as_view()),
    url(r'^filter/$', FilterTaskAPIView.as_view())
]
