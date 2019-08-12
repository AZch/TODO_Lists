from django.conf.urls import url

from todo.APIViews.FilterTaskAPIView import FilterTaskAPIView
from todo.APIViews.TodoUserAPIView import TodoUserAPIView
from .views import *

app_name = 'todo'

urlpatterns = [
    url(r'^(?P<id>\d+)/', TodoUserAPIView.as_view()),
    url(r'^create/', create_todo),
    url(r'^all/', get_all_todo),
    url(r'^filter/$', FilterTaskAPIView.as_view())
]
