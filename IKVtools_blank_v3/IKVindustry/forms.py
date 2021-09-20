from django import forms
from django.forms.models import inlineformset_factory, modelformset_factory

from .models import Industry, IndustryFiles, WorkPackage, Outgoings
from .widgets import CFI, Price, Percent, SelectAssistant, DatePicker


class IndustryForm(forms.ModelForm):
    class Meta:
        model = Industry
        exclude = ()
        widgets = {
            'fanr': forms.TextInput(attrs={'class':'form-control ', 'placeholder': 'FA-Nummer'}),
            'company': forms.TextInput(attrs={'class':'form-control ', 'placeholder': 'Firma'}),
            'title': forms.TextInput(attrs={'class':'form-control ', 'placeholder': 'Titel'}),
            'short_title': forms.TextInput(attrs={'class':'form-control ', 'placeholder': 'Kurztitel'}),
            'kind': forms.Select(attrs={'class':'form-control ', 'placeholder ': 'Art'}),
            'finish_finance_a': DatePicker(attrs={'class': 'form-control datetimepicker-input ', 'data-target':'#finishFinance', 'data-toggle':'datetimepicker'}),
            'finish_finance_al': DatePicker(attrs={'class': 'form-control datetimepicker-input ', 'data-target':'#finishFinance', 'data-toggle':'datetimepicker'}),
            'finish_finance_s': DatePicker(attrs={'class': 'form-control datetimepicker-input ', 'data-target':'#finishFinance', 'data-toggle':'datetimepicker'}),
            'status': forms.Select(attrs={'class':'form-control ', 'placeholder': 'Status'}),
            'released': forms.CheckboxInput(attrs={'class':'form-control ', 'placeholder': 'Freigegeben'})
        }


class WorkPackagesForm(forms.ModelForm):
    class Meta:
        model = WorkPackage
        exclude = ()
        widgets = {
            'assistant_id': SelectAssistant(attrs={'class':'form-control select2bs4', 'placeholder': 'Bearbeiter'}),
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Teilschritt'}),
            'material': Percent(attrs={'class':'form-control', 'placeholder': 'Material [%]'}),
            'staff': Percent(attrs={'class':'form-control', 'placeholder': 'Personal [%]'}),
            'instruct_at': DatePicker(attrs={'class': 'form-control datetimepicker-input', 'placeholder': 'Beauftragt am'}),
            'invoiced_at': DatePicker(attrs={'class': 'form-control datetimepicker-input', 'placeholder': 'Fakturiert am'}),
            'price': Price(attrs={'class':'form-control', 'placeholder': 'Kosten'}),
            'foreign': forms.CheckboxInput(attrs={'class':'form-control', 'placeholder': 'Fremdleistung'}),
        }


class IndustryFilesForm(forms.ModelForm):
    class Meta:
        model = IndustryFiles
        exclude = ()
        widgets = {
            'file': CFI(attrs={'class':'form-control col-sm-10', 'placeholder': 'Datei'}),
            'description': forms.TextInput(attrs={'class':'form-control col-sm-10', 'placeholder': 'Beschreibung'}),
        }


class OutgoingsForm(forms.ModelForm):
    class Meta:
        model = Outgoings
        exclude = ()
        widgets = {
            'price' : Price(attrs={'class':'form-control', 'placeholder':'Preis'}),
            'description' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Beschreibung'}),
            'kind' : forms.Select(attrs={'class':'form-control', 'placeholder':'Budget'}),
            'added' : forms.DateInput(attrs={'class':'form-control', 'placeholder':'Hinzugefügt'}),
        }

WorkPackageFormSet = inlineformset_factory(Industry, WorkPackage, form=WorkPackagesForm, extra=1)
IndustryFilesFormSet = inlineformset_factory(Industry, IndustryFiles, form=IndustryFilesForm, extra=4)
OutgoingsFormSet = inlineformset_factory(Industry, Outgoings, form=OutgoingsForm, extra=1)