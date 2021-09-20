"""IKVtools URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import Index, Settings
import IKVassistant, IKVpublic, IKVindustry, IKVpublication, IKVstudents, IKVprotocol

app_name = 'IKVtools'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('IKVassistant/', include('IKVassistant.urls', 'IKVassistant')),
    path('IKVindustry/', include('IKVindustry.urls', 'IKVindustry')),
    path('IKVpublic/', include('IKVpublic.urls', 'IKVpublic')),
    path('IKVpublication/', include('IKVpublication.urls', 'IKVpublication')),
    path('IKVprotocol/', include('IKVprotocol.urls', 'IKVprotocol')),
    path('IKVstudents', include('IKVstudents.urls'), name='IKVstudents'),
    path('settings/', Settings.as_view(), name='settings'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
