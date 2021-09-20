from django.urls import path
from .views import PublicationListView, PublicationUpdateView, SettingsAuthor, SettingsJournal

app_name = 'IKVpublication'


urlpatterns = [
    path('', PublicationListView.as_view(), name='list'),
    path('update/<int:pk>', PublicationUpdateView.as_view(), name='update'),
    path('settings/author', SettingsAuthor.as_view(), name='settings_author'),
    path('settings/journal', SettingsJournal.as_view(), name='settings_journal')
    
]