from django.urls import path
from . import views
from django.contrib.auth import views as authViews


urlpatterns = [
    path('', views.index, name='home'),
    path('account', views.account, name='account'),
    path('exit/', authViews.LogoutView.as_view(next_page='home'), name='exit'),
    path('add-funds', views.add_funds, name='add-funds'),
]
