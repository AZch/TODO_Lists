from django.conf.urls import url

from users.APIViews.CreateUserAPIView import CreateUserAPIView
from users.APIViews.FilterTaskAPIView import FilterTaskAPIView
from users.APIViews.TodoUserAPIView import TodoUserAPIView
from users.APIViews.UserRetrieveUpdateAPIView import UserRetrieveUpdateAPIView
from .views import *

app_name = 'users'

urlpatterns = [
    url(r'^create/$', CreateUserAPIView.as_view()),
    url(r'^obtain_token', authenticate_user),
    url(r'^update/$', UserRetrieveUpdateAPIView.as_view()),
    url(r'^todo/$', TodoUserAPIView.as_view()),
    url(r'^filter/$', FilterTaskAPIView.as_view())
]
