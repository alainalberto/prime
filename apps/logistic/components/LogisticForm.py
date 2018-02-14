from django import forms
from apps.logistic.models import *
from apps.services.models import Application



class LoadsForm(forms.ModelForm):
    class Meta:
        model = Load

        fields = [
            'broker',
            'pickup_from',
            'pickup_date',
            'deliver',
            'dispatch',
            'driver',
            'deliver_date',
            'value',
            'number',
            'paid',
            'note',
            'other_company'
        ]
        labels = {
            'broker': 'Broker Name:',
            'pickup_from': 'Pick up From:',
            'pickup_date': 'Pick up Date:',
            'deliver': 'Deliver to:',
            'deliver_date': 'Deliver Date:',
            'dispatch': 'Dispatch:',
            'driver': 'Driver:',
            'value': 'Agreed Amount:',
            'number': 'Load Number:',
            'paid': 'Is Paid:',
            'note': 'Note:',
        }
        widgets = {
            'broker': forms.TextInput(attrs={'placeholder': 'Broker', 'class': 'form-control input-md upper', 'required': 'true'}),
            'pickup_from': forms.TextInput(attrs={'placeholder': 'Pick up From', 'class': 'form-control input-md upper'}),
            'pickup_date': forms.DateInput(attrs={'class': 'form-control input-md'}),
            'deliver': forms.TextInput(attrs={'placeholder': 'Deliver to', 'class': 'form-control input-md upper'}),
            'deliver_date': forms.DateInput(attrs={'class': 'form-control input-md'}),
            'dispatch': forms.Select(attrs={'class': 'form-control input-md', 'required': 'true'}),
            'driver': forms.Select(attrs={'class': 'form-control input-md', 'required': 'true'}),
            'value': forms.NumberInput(attrs={'placeholder': 'Value', 'class': 'form-control input-md'}),
            'number': forms.TextInput(attrs={'placeholder': 'Number', 'class': 'form-control input-md', 'required': 'true'}),
            'paid': forms.CheckboxInput(attrs={'data-off-color':"danger", 'class':"switch", 'data-size':"mini", 'data-on-text':"YES", 'data-off-text': "NO"}),
            'note': forms.Textarea(attrs={'class': 'form-control'}),
            'other_company': forms.CheckboxInput(
                attrs={'id': "id_other_company", 'data-toggle': "toggle", 'type': "checkbox", 'data-on': "Other Company",
                       'data-off': "This Company"}),

        }


class DriversForm(forms.ModelForm):
    class Meta:
        model = DriversLogt

        fields = [
            'name',
            'owner_name',
            'license_numb',
            'address',
            'email',
            'ssn',
            'dob',
            'lic_date_exp',
            'medicard_date_exp',
            'drugtest_date',
            'drugtest_date_exp',
            'mbr_date',
            'mbr_date_exp',
            'begining_date',
            'deactivate',
            'type',
            'dow_payment',
            'escrow',
        ]
        labels = {
            'name': 'Name:',
            'owner_name': 'Owner Full Name:',
            'license_numb': 'License Number:',
            'address': 'Address:',
            'email': 'Email:',
            'ssn': 'SSN:',
            'dob': 'DOB:',
            'lic_date_exp': 'License Date Expirate:',
            'medicard_date_exp': 'Medicard Date Expirate:',
            'drugtest_date': 'Drug Test Date:',
            'drugtest_date_exp': 'Drug Test Date Expirate:',
            'mbr_date': 'MVR Date:',
            'mbr_date_exp': 'MBR Date Expirate:',
            'begining_date': 'Beginning Date:',
            'deactivate': 'Deactivate:',
            'type': 'Type:',
            'dow_payment': 'Dow Payment:',
            'escrow': 'Escrow:',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control input-md upper', 'required': 'true'}),
            'owner_name': forms.TextInput(attrs={'placeholder': 'Owner Name', 'class': 'form-control input-md upper'}),
            'license_numb': forms.NumberInput(attrs={'placeholder': 'License Number', 'class': 'form-control input-md', 'required': 'true'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control input-md upper'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email', 'class': 'form-control input-md'}),
            'ssn': forms.PasswordInput(attrs={'class': 'form-control input-md'}),
            'dob': forms.DateInput(attrs={'class': 'form-control input-md'}),
            'lic_date_exp': forms.DateInput(attrs={'class': 'form-control input-md'}),
            'medicard_date_exp': forms.DateInput(attrs={'class': 'form-control input-md'}),
            'drugtest_date': forms.DateInput(attrs={'class': 'form-control input-md'}),
            'drugtest_date_exp': forms.DateInput(attrs={'class': 'form-control input-md'}),
            'mbr_date': forms.DateInput(attrs={'class': 'form-control input-md'}),
            'mbr_date_exp': forms.DateInput(attrs={'class': 'form-control input-md'}),
            'begining_date': forms.DateInput(attrs={'class': 'form-control input-md'}),
            'deactivate': forms.CheckboxInput(attrs={'data-off-color':"danger", 'class':"switch", 'data-size':"mini", 'data-on-text':"YES", 'data-off-text': "NO"}),
            'type': forms.Select(attrs={'class': 'form-control input-md'}, choices=(('Driver','Driver'), ('Owner Operation','Owner Operation'))),
            'dow_payment': forms.NumberInput(attrs={'placeholder': 'Dow Payment', 'class': 'form-control input-md'}),
            'escrow': forms.NumberInput(attrs={'placeholder': 'Escrow', 'class': 'form-control input-md'}),
        }


class DispatchForm(forms.ModelForm):
    class Meta:
        model = DispatchLogt

        fields = [
            'name',
            'address',
            'comission',
            'deactivate',
            'date_deactivated',
        ]
        labels = {
            'name': 'Name:',
            'address': 'Address:',
            'comission': 'Comission:',
            'deactivate': 'Deactivate:',
            'date_deactivated': 'Deactivate Date:',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control input-md upper', 'required': 'true'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control input-md upper'}),
            'comission': forms.NumberInput(attrs={'placeholder': 'Porcent', 'class': 'form-control input-md', 'required': 'true'}),
            'deactivate': forms.CheckboxInput(attrs={'data-off-color':"danger", 'class':"switch", 'data-size':"mini", 'data-on-text':"YES", 'data-off-text': "NO"}),
            'date_deactivated': forms.DateInput(attrs={'class': 'form-control input-md'}),

        }

class DieselForm(forms.ModelForm):
    class Meta:
        model = Diesel

        fields = [
            'driver',
            'date_start',
            'date_end',
            'total',
        ]

        widgets = {
            'driver': forms.Select(attrs={'class': 'form-control input-md'}),
            'date_start': forms.DateInput(attrs={'class': 'form-control input-md'}),
            'date_end': forms.DateInput(attrs={'class': 'form-control input-md'}),
            'total': forms.NumberInput(attrs={'placeholder': 'Total', 'class': 'form-control input-md', 'required': 'true'}),
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application

        fields = [
            'fullname',
            'company_name',
            'address',
            'phone',
            'no_social',
            'email',
            'license_numb',
            'usdot',
            'mc',
            'txdmv',
            'ein',
            'service',
            'note',
            'state',
        ]
        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'form-control input-md upper'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control input-md upper'}),
            'address': forms.TextInput(attrs={'class': 'form-control input-md upper'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control input-md upper'}),
            'no_social': forms.TextInput(attrs={'class': 'form-control input-md upper'}),
            'email': forms.EmailInput(attrs={'class': 'form-control input-md upper'}),
            'license_numb': forms.TextInput(attrs={'class': 'form-control input-md upper'}),
            'usdot': forms.TextInput(attrs={'class': 'form-control input-md upper'}),
            'mc': forms.TextInput(attrs={'class': 'form-control input-md upper'}),
            'txdmv': forms.TextInput(attrs={ 'class': 'form-control input-md upper'}),
            'ein': forms.TextInput(attrs={'class': 'form-control input-md upper'}),
            'service': forms.NumberInput(attrs={'class': 'form-control input-md upper'}),
            'note': forms.Textarea(attrs={'class': 'form-control input-md upper'}),
            'state':forms.Select(attrs={'class': 'form-control input-md'}, choices=(('Request','Request'), ('Viewed','Viewed'),('Approved','Approved'),('Rejected','Rejected'),)),
        }