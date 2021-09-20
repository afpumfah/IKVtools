from django import forms
from django.forms.models import inlineformset_factory, modelformset_factory

from IKVassistant.models import Assistant

from .models import Protocol, ToDo
from .widgets import SelectProject, CSM, SelectAssistant, DatePicker


class ProtocolForm(forms.ModelForm):
    class Meta:
        model = Protocol
        exclude = ()
        widgets = {
            'public_project_id': SelectProject(attrs={'class':'form-control select2bs4', 'placeholder': 'Öffentliches Projekt'}),
            'industry_project_id': SelectProject(attrs={'class':'form-control select2bs4', 'placeholder': 'Industrieprojekt'}),
            'title': forms.Textarea(attrs={'class':'form-control', 'rows':2, 'placeholder': 'Titel'}),
            'place': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Ort'}),
            'content': forms.Textarea(attrs={'class':'textarea', 'placeholder': 'Zusammenfassung'}),
            'date': DatePicker(attrs={'class':'form-control', 'placeholder': 'Wann'}),
        }
    assistant_id = forms.ModelMultipleChoiceField(Assistant.objects.all(), widget=CSM(attrs={'class':'form-control select2bs4'}), label='Assistent')


class TodoForm(forms.ModelForm):
    class Meta:
        model = ToDo
        exclude = ()
        widgets = {
            'assistant_id': SelectAssistant(attrs={'class':'form-control select2bs4', 'placeholder': 'Assistent'}),
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Was?'}),
            'duedate': DatePicker(attrs={'class':'form-control', 'placeholder': 'Fällig am'}),
            'done': forms.CheckboxInput(attrs={'class':'form-control ', 'placeholder': 'erledigt'})
        }


ProtocolFormSet = inlineformset_factory(Protocol, ToDo, form=TodoForm, extra=1)