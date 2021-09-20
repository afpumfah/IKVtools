from django.urls import path
from .views import IndustryListView, IndustryDetailView, IndustryUpdateView, IndustryUpdateFileView, IndustryUpdateOutgoingsView, IndustryUpdateWorkPackageView, IndustryProtocol

app_name = 'IKVindustry'


urlpatterns = [
    path('', IndustryListView.as_view(), name='list'),
    path('<int:pk>/', IndustryDetailView.as_view(), name='detail'),
    path('update/<int:pk>', IndustryUpdateView.as_view(), name='update'),
    path('update/files/<int:pk>', IndustryUpdateFileView.as_view(), name='update_file'),
    path('update/workpackage/<int:pk>', IndustryUpdateWorkPackageView.as_view(), name='update_workpackage'),
    path('update/outgoings/<int:pk>', IndustryUpdateOutgoingsView.as_view(), name='update_outgoing'),
    path('protocol/<int:pk>', IndustryProtocol.as_view(), name='protocol'),
    
]