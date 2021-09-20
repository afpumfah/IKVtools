from django import forms
from django.forms.models import inlineformset_factory, modelformset_factory

from .models import Student, StudentAssistant, Thesis, MeanPrice
from .widgets import Price, DatePicker, Hours, SelectAssistant, CSM


from IKVassistant.models import Assistant

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ()
        widgets = {
            'firstname':forms.TextInput(attrs={'class':'form-control ', 'placeholder': 'Vorname'}),
            'lastname':forms.TextInput(attrs={'class':'form-control ', 'placeholder': 'Nachname'}),
            
        }


class StudentAssistantForm(forms.ModelForm):
    class Meta:
        model = StudentAssistant
        exclude = ()
        widgets = {
            'student_id': SelectAssistant(attrs={'class':'form-control select2bs4', 'placeholder': 'Student'}),
            'assistant_id': SelectAssistant(attrs={'class':'form-control select2bs4 ', 'placeholder': 'Assistent'}),
            'status':forms.Select(attrs={'class':'form-control ', 'placeholder': 'Status'}),
            'hours':Hours(attrs={'class':'form-control ', 'placeholder': 'Stunden'}),
            'price':Price(attrs={'class':'form-control ', 'placeholder': 'Kosten'}),
            'start':DatePicker(attrs={'class':'form-control ', 'placeholder': 'Start'}),
            'end':DatePicker(attrs={'class':'form-control ', 'placeholder': 'Ende'}),
        }


class ThesisForm(forms.ModelForm):

    class Meta:
        model = Thesis
        exclude = ()
        widgets = {
            'student_id': SelectAssistant(attrs={'class':'form-control select2bs4', 'placeholder': 'Student'}),
            'title': forms.TextInput(attrs={'class':'form-control ', 'placeholder': 'Titel'}),
            'type':forms.Select(attrs={'class':'form-control ', 'placeholder': 'Art der Arbeit'}),
            'release_date':DatePicker(attrs={'class':'form-control ', 'placeholder': 'Erscheinungsdatum'}),
        }
    
    supervisor_id = forms.ModelMultipleChoiceField(Assistant.objects.all(), widget=CSM(attrs={'class':'form-control select2bs4'}), label='Betreuer')


class PriceForm(forms.Form):

    mean_price = forms.CharField(label='Mittlerer Finanzierungswert', widget=Price(attrs={'class':'form-control ', 'placeholder': 'Mittlerer Preis'}))
    shk_07 = forms.CharField(label='SHK 7', widget=Price(attrs={'class':'form-control ', 'placeholder': 'SHK7'}))
    shk_08 = forms.CharField(label='SHK 8', widget=Price(attrs={'class':'form-control ', 'placeholder': 'SHK8'}))
    shk_09 = forms.CharField(label='SHK 9', widget=Price(attrs={'class':'form-control ', 'placeholder': 'SHK9'}))
    shk_10 = forms.CharField(label='SHK 10', widget=Price(attrs={'class':'form-control ', 'placeholder': 'SHK10'}))
    shk_11 = forms.CharField(label='SHK 11', widget=Price(attrs={'class':'form-control ', 'placeholder': 'SHK11'}))
    shk_12 = forms.CharField(label='SHK 12', widget=Price(attrs={'class':'form-control ', 'placeholder': 'SHK12'}))
    shk_13 = forms.CharField(label='SHK 13', widget=Price(attrs={'class':'form-control ', 'placeholder': 'SHK13'}))
    shk_14 = forms.CharField(label='SHK 14', widget=Price(attrs={'class':'form-control ', 'placeholder': 'SHK14'}))
    shk_15 = forms.CharField(label='SHK 15', widget=Price(attrs={'class':'form-control ', 'placeholder': 'SHK15'}))
    shk_16 = forms.CharField(label='SHK 16', widget=Price(attrs={'class':'form-control ', 'placeholder': 'SHK16'}))
    shk_17 = forms.CharField(label='SHK 17', widget=Price(attrs={'class':'form-control ', 'placeholder': 'SHK17'}))
    shk_18 = forms.CharField(label='SHK 18', widget=Price(attrs={'class':'form-control ', 'placeholder': 'SHK18'}))
    shk_19 = forms.CharField(label='SHK 19', widget=Price(attrs={'class':'form-control ', 'placeholder': 'SHK19'}))

    whk_07 = forms.CharField(label='WHK 7', widget=Price(attrs={'class':'form-control ', 'placeholder': 'WHK7'}))
    whk_08 = forms.CharField(label='WHK 8', widget=Price(attrs={'class':'form-control ', 'placeholder': 'WHK8'}))
    whk_09 = forms.CharField(label='WHK 9', widget=Price(attrs={'class':'form-control ', 'placeholder': 'WHK9'}))
    whk_10 = forms.CharField(label='WHK 10', widget=Price(attrs={'class':'form-control ', 'placeholder': 'WHK10'}))
    whk_11 = forms.CharField(label='WHK 11', widget=Price(attrs={'class':'form-control ', 'placeholder': 'WHK11'}))
    whk_12 = forms.CharField(label='WHK 12', widget=Price(attrs={'class':'form-control ', 'placeholder': 'WHK12'}))
    whk_13 = forms.CharField(label='WHK 13', widget=Price(attrs={'class':'form-control ', 'placeholder': 'WHK13'}))
    whk_14 = forms.CharField(label='WHK 14', widget=Price(attrs={'class':'form-control ', 'placeholder': 'WHK14'}))
    whk_15 = forms.CharField(label='WHK 15', widget=Price(attrs={'class':'form-control ', 'placeholder': 'WHK15'}))
    whk_16 = forms.CharField(label='WHK 16', widget=Price(attrs={'class':'form-control ', 'placeholder': 'WHK16'}))
    whk_17 = forms.CharField(label='WHK 17', widget=Price(attrs={'class':'form-control ', 'placeholder': 'WHK17'}))
    whk_18 = forms.CharField(label='WHK 18', widget=Price(attrs={'class':'form-control ', 'placeholder': 'WHK18'}))
    whk_19 = forms.CharField(label='WHK 19', widget=Price(attrs={'class':'form-control ', 'placeholder': 'WHK19'}))


StudentAssistantFormSet = inlineformset_factory(Student, StudentAssistant, form=StudentAssistantForm, extra=1)
ThesisFormSet = inlineformset_factory(Student, Thesis, form=ThesisForm, extra=1)