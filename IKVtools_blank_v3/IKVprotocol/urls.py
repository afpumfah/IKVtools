from django.urls import path

app_name = 'IKVprotocol'

from .views import ProtocolListView, ProtocolUpdateView


urlpatterns = [
    path('', ProtocolListView.as_view(), name='list'),
    path('update/<int:pk>', ProtocolUpdateView.as_view(), name='update'),
]