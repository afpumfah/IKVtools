from django import forms
from django.forms.models import inlineformset_factory, modelformset_factory

from .models import Public, PublicAssistant, PublicFiles, PublicWorkPackage, Financier
from .widgets import DatePicker, SelectAssistant, CFI, Color, CSM

from IKVassistant.models import Assistant


class PublicForm(forms.ModelForm):
    class Meta:
        model = Public
        exclude = ()
        widgets = {
            'fanr': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'FA-Nummer'}),
            'financier': forms.Select(attrs={'class':'form-control', 'placeholder': 'Geldgeber'}),
            'project_number': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Förderkennzeichen'}),
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Titel'}),
            'short_title': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Kurztitel'}),
            'start': DatePicker(attrs={'class':'form-control', 'placeholder': 'Projektstart'}),
            'end': DatePicker(attrs={'class':'form-control', 'placeholder': 'Projektende'}),
            'al_date': DatePicker(attrs={'class':'form-control', 'placeholder': 'AL-Datum'}),
            'gl_date': DatePicker(attrs={'class':'form-control', 'placeholder': 'GL-Datum'}),
            'status': forms.Select(attrs={'class':'form-control', 'placeholder': 'Status'}),
            'funded_position': forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Finanzierte Stellen'}),
            'funded_students': forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Finanzierte HiWis'}),
            'summary': forms.Textarea(attrs={'class':'textarea', 'placeholder': 'Zusammenfassung'}),
        }


class PublicAssistantForm(forms.ModelForm):
    class Meta:
        model = PublicAssistant
        exclude = ()
        widgets = {
            'assistant_id': SelectAssistant(attrs={'class':'form-control select2bs4', 'placeholder': 'Bearbeiter'}),
            'start': DatePicker(attrs={'class':'form-control', 'placeholder': 'Projektstart'}),
            'end': DatePicker(attrs={'class':'form-control', 'placeholder': 'Projektende'}),
        }


class PublicFilesForm(forms.ModelForm):
    class Meta:
        model = PublicFiles
        exclude = ()
        widgets = {
            'file': CFI(attrs={'class':'form-control', 'placeholder': 'Datei'}),
            'description': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Beschreibung'}),
        }


class PublicWorkPackageForm(forms.ModelForm):
    class Meta:
        model = PublicWorkPackage
        exclude = ()
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Beschreibung'}),
            'start': DatePicker(attrs={'class':'form-control', 'placeholder': 'Arbeitspaket (Start)'}),
            'end': DatePicker(attrs={'class':'form-control', 'placeholder': 'Arbeitspaket (Ende)'}),
        }


class FinancierForm(forms.ModelForm):
    class Meta:
        model = Financier
        exclude = ()
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Geldgeber'}),
            'image': CFI(attrs={'class':'form-control', 'placeholder': 'Bild'}),
            'color': Color(attrs={'class':'form-control', 'placeholder': 'Farbe'}),
        }

PublicAssistantFormSet = inlineformset_factory(Public, PublicAssistant, form=PublicAssistantForm, extra=1)
PublicFilesFormSet = inlineformset_factory(Public, PublicFiles, form=PublicFilesForm, extra=5)
PublicWorkPackageFormSet = inlineformset_factory(Public, PublicWorkPackage, form=PublicWorkPackageForm, extra=5)