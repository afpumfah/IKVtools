from django.urls import path
from .views import AssistantListView, AssistantDetailView, AssistantUpdateView, AssistantUpdateFilesView, AssistantProtocol

app_name = 'IKVassistant'


urlpatterns = [
    path('', AssistantListView.as_view(), name='list'),
    path('<int:pk>/', AssistantDetailView.as_view(), name='detail'),
    path('update/<int:pk>', AssistantUpdateView.as_view(), name='update'),
    path('update/files/<int:pk>', AssistantUpdateFilesView.as_view(), name='update_files'),
    path('protocol/<int:pk>', AssistantProtocol.as_view(), name='protocol')
    
]