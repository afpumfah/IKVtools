from django import forms
from django.forms.models import inlineformset_factory, modelformset_factory

from .models import Publication, Author, Journal
from .widgets import SelectAssistant, DatePicker, SelectProject, CSM

from IKVassistant.models import Assistant

from itertools import chain

class PublicationForm(forms.ModelForm):
    

    class Meta:
        model = Publication
        exclude = ()
        widgets = {
            'publicproject_id': SelectProject(attrs={'class':'form-control select2bs4', 'placeholder': 'Öffentliches Projekt'}),
            'title': forms.Textarea(attrs={'class':'form-control', 'rows':2, 'placeholder': 'Titel'}),
            'journal': SelectProject(attrs={'class':'form-control select2bs4', 'placeholder': 'Journal'}),
            'release_date': DatePicker(attrs={'class':'form-control', 'placeholder': 'Erscheinungsdatum'}),
            'status': forms.Select(attrs={'class':'form-control select2bs4', 'placeholder': 'Status'}),
            'reviewed': forms.Select(attrs={'class':'form-control select2bs4', 'placeholder': 'Art der Veröffentlichung'}),
        }

    assistant_id = forms.ModelMultipleChoiceField(Assistant.objects.all(), widget=CSM(attrs={'class':'form-control select2bs4'}), label='Assistent')
    author_id = forms.ModelMultipleChoiceField(Author.objects.all(), widget=CSM(attrs={'class':'form-control select2bs4'}), label='Weitere Autoren')


class AuthorForm(forms.ModelForm):
    
    class Meta:
        model = Author
        exclude = ()
        widgets = {
            'firstname': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Vorname'}),
            'lastname': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Nachname'}),
        }


class JournalForm(forms.ModelForm):
    
    class Meta:
        model = Journal
        exclude = ()
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Journal'}),
        }

