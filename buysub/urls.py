from django.urls import path
from . import views


urlpatterns = [
    path('subscriptions', views.subscriptions, name='subscriptions'),
    path('confirm-buy', views.confirm_buy, name='confirm-buy'),
]