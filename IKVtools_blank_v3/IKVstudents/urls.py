from django.urls import path
from .views import StudentListView, StudentUpdateView, PriceUpdateView

app_name = 'IKVstudents'


urlpatterns = [
    path('', StudentListView.as_view(), name='list'),
    path('update/<int:pk>', StudentUpdateView.as_view(), name='update'),
    path('settings/meanprice/', PriceUpdateView.as_view(), name='settings_meanprice'),
]