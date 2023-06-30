from django.urls import path
from . import views


urlpatterns = [
    path('bit-float', views.bit_float, name='bit-float'),
]