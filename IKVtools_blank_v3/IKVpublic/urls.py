from django.urls import path
from .views import PublicDetailView, PublicListView, PublicUpdateView, PublicUpdateFileView, PublicUpdateAssistantView, PublicUpdateWorkPackageView, FinancierView, FinancierUpdateView, PublicProtocol

app_name = 'IKVpublic'


urlpatterns = [
    path('', PublicListView.as_view(), name='list'),
    path('<int:pk>/', PublicDetailView.as_view(), name='detail'),
    path('update/<int:pk>', PublicUpdateView.as_view(), name='update'),
    path('update/file/<int:pk>', PublicUpdateFileView.as_view(), name='update_file'),
    path('update/assistant/<int:pk>', PublicUpdateAssistantView.as_view(), name='update_assistant'),
    path('update/workpackage/<int:pk>', PublicUpdateWorkPackageView.as_view(), name='update_workpackage'),
    path('protocol/<int:pk>', PublicProtocol.as_view(), name='protocol'),
    path('settings/financier/', FinancierView.as_view(), name='settings_financier'),
    path('settings/financier/update/<int:pk>', FinancierUpdateView.as_view(), name='settings_financier_update'),
]