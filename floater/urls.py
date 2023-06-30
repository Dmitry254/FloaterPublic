from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('', include('main.urls')),
    path('', include('signin.urls')),
    path('', include('market.urls')),
    path('', include('bitskins.urls')),
    path('', include('bitpattern.urls')),
    path('', include('marketpattern.urls')),
    path('', include('buysub.urls')),
    path('', include('finditem.urls')),
)
