from django import forms
from .models import Patients

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetimepicker.widgets import DateTimePicker


class AdjustPayed(forms.Form):
    payed = forms.DecimalField(label='', required=False)
        
class CalendarPickerForm(forms.Form):
     month = forms.ChoiceField(choices=[(x,x) for x in range(1,13)])

class AddPatientForm(forms.Form):
    """form to add patient"""
    last_name = forms.CharField(label='Nom*', max_length=40)
    first_name = forms.CharField(label='Prénom*', max_length=40)
    birthday = forms.DateField(label='date de naissance*',
    	widget=forms.DateInput(format='%d/%m/%Y',attrs={'placeholder': '31/03/1989'}),
    	input_formats=['%d/%m/%Y',])

    tel = forms.CharField(label='tel', max_length=20, required=False)
    mail = forms.CharField(label='mail', max_length=80, required=False)  # Modif pour données encodées côté client
    notes = forms.CharField(label='notes',widget=forms.Textarea, required=False)

class EditPatient(forms.Form):
    tel = forms.CharField(label='tel', max_length=20, required=False)
    mail = forms.CharField(label='mail', max_length=80, required=False)

class EditNote(forms.Form):
    #notes = forms.CharField(label='notes', required=False)
    #notes =  forms.Textarea()
    notes = forms.CharField(label='notes',widget=forms.Textarea(attrs={'rows':12, 'cols':40}))


class RecordForm(forms.Form):
    """form to record a consultation"""
    class Meta:
        model = Patients

    def __init__(self, user, *args, **kwargs):
        super(RecordForm, self).__init__(*args, **kwargs)
        self.fields['Patient'] = forms.ModelChoiceField(queryset=Patients.objects.filter(owner_id=user,active=True)) 
        self.fields['date'] = forms.DateTimeField(label= 'Date (laisser vide si date et heure actuelles)',
                                                    input_formats=['%d/%m/%Y %H:%M'], 
                                                    required=False) 
        #self.fields['payed'] = forms.BooleanField(label='A payé lors de la consultation', required=False)
        self.fields['tarif'] = forms.DecimalField(label="Tarif (laisser vide si consultation impayée)", required=False, ) # amélioration possible: valeur par défault dépendant des consultations passées

class GetByPatients(forms.Form):
    class Meta:
        model = Patients

    def __init__(self, user, *args, **kwargs):
        super(GetByPatients, self).__init__(*args, **kwargs)
        self.fields['Patient'] = forms.ModelChoiceField(queryset=Patients.objects.filter(owner_id=user)) 


# pas sur que celui ci serve encore
class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('email', 'username')
		