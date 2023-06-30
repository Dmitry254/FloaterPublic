from django.urls import path
from . import views


urlpatterns = [
    path('find-item', views.find_item, name='find-item'),
]