from django.conf.urls import url

from .views import CreateUserAPIView, authenticate_user, UserRetrieveUpdateAPIView

app_name = 'users'

urlpatterns = [
    url(r'^create/$', CreateUserAPIView.as_view()),
    url(r'^test_token', authenticate_user),
    url(r'^update/$', UserRetrieveUpdateAPIView.as_view()),
]
