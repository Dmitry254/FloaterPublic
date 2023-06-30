from django.urls import path
from . import views


urlpatterns = [
    path('bit-patterns', views.bit_patterns, name='bit-patterns'),
]