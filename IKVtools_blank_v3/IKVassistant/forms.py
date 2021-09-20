from django import forms
from django.forms.models import inlineformset_factory

from .models import Assistant, AssistantFiles
from .widgets import DatePicker, Mail, Phone, CFI


class AssistantForm(forms.ModelForm):
    class Meta:
        model = Assistant
        exclude = ()
        widgets = {
            'firstname': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Vorname'}),
            'lastname': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Nachname'}),
            'email': Mail(attrs={'class':'form-control', 'placeholder': 'Email'}),
            'phone': Phone(attrs={'class':'form-control', 'placeholder': 'Nummer +49 241 80 -'}),
            'birth': DatePicker(attrs={'class':'form-control', 'placeholder': 'Geburtstag'}),
            'start': DatePicker(attrs={'class':'form-control', 'placeholder': 'Einstieg'}),
            'end': DatePicker(attrs={'class':'form-control', 'placeholder': 'Ausstieg'}),
            'status': forms.Select(attrs={'class':'form-control', 'placeholder': 'Status'}),
        }


class AssistantFilesForm(forms.ModelForm):
    class Meta:
        model = AssistantFiles
        exclude = ()
        widgets = {
            'file': CFI(attrs={'class':'form-control', 'placeholder': 'Datei'}),
            'description': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Beschreibung'}),
        }

AssistantFormSet = inlineformset_factory(Assistant, AssistantFiles, form=AssistantFilesForm, extra=5)