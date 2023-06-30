from django.urls import path
from . import views


urlpatterns = [
    path('market-float', views.market_float, name='market-float'),
]
