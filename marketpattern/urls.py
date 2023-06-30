from django.urls import path
from . import views


urlpatterns = [
    path('market-patterns', views.market_patterns, name='market-patterns'),
]