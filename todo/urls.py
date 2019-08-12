from django.conf.urls import url

from todo.APIViews.FilterTaskAPIView import FilterTaskAPIView
from .views import *

app_name = 'todo'

urlpatterns = [
    url(r'^<int:id>', get_all_todo),
    url(r'^filter/$', FilterTaskAPIView.as_view())
]
