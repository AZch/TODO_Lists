from django.conf.urls import url

from .views import *

app_name = 'users'

urlpatterns = [
    url(r'^create/$', CreateUserAPIView.as_view()),
    url(r'^test_token', authenticate_user),
    url(r'^update/$', UserRetrieveUpdateAPIView.as_view()),
    url(r'^task/$', TodoUserAPIView.as_view())
]
