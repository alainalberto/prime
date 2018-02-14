from django import forms
from django.urls import reverse
from django.utils.safestring import mark_safe
from apps.services.models import *
from apps.tools.models import File

class PermitForm(forms.ModelForm):

    class Meta:
        model = Permit

        fields = [
                  'is_new',
                  'legal_status',
                  'gusiness_type',
                  'name',
                  'attorney',
                  'otheattorney',
                  'address',
                  'phone',
                  'othephone',
                  'fax',
                  'ein',
                  'unit',
                  'usdot',
                  'usdot_pin',
                  'txdmv',
                  'txdmv_user',
                  'txdmv_passd',
                  'txdmv_date',
                  'txdmv_date_exp',
                  'mc',
                  'mc_pin',
                  'boc3',
                  'boc3_date',
                  'ucr',
                  'ucr_date_exp',
                  'account_number',
                  'account_user',
                  'account_password',
                  'inter',
                  'deactivate',
                  'state',
                  'customers',
        ]

        widgets = {
            'is_new': forms.CheckboxInput(attrs={'data-off-color':"danger", 'class':"switch", 'data-size':"mini", 'data-on-text':"YES", 'data-off-text': "NO"}),
            'legal_status': forms.Select(attrs={'class': 'form-control input-md', 'required':'true', 'title':'Select one'}, choices=(('DBA', 'DBA'), ('LLC', 'LLC'), ('CORP', 'CORP'))),
            'gusiness_type': forms.Select(attrs={'class': 'form-control input-md'}, choices=(('Flatbed', 'Flatbed'), ('Refrigerated', 'Refrigerated'), ('Dry Van', 'Dry Van'), ('Sand Gravel', 'Sand Gravel'), ('Other', 'Other'))),
            'name': forms.TextInput(attrs={'placeholder': 'Company Name', 'class': 'form-control input-md upper', 'required':'true', 'title':'Inset Name'}),
            'attorney': forms.TextInput(attrs={'placeholder': 'Authorized Person:', 'class':'form-control input-md upper'}),
            'otheattorney': forms.TextInput(attrs={'placeholder': 'Authorized Person:', 'class':'form-control input-md upper'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control input-md upper'}),
            'phone': forms.NumberInput(attrs={'placeholder': 'Telepone Number', 'class': 'form-control input-md'}),
            'othephone': forms.NumberInput(attrs={'placeholder': 'Telepone Number', 'class': 'form-control input-md'}),
            'fax': forms.NumberInput(attrs={'placeholder': 'Fax Number', 'class': 'form-control input-md'}),
            'ein': forms.NumberInput(attrs={'placeholder': 'EIN', 'class': 'form-control input-md', 'required':'true', 'title':'Inset EIN'}),
            'unit': forms.NumberInput(attrs={'placeholder': 'Unit', 'class': 'form-control input-md'}),
            'usdot': forms.NumberInput(attrs={'placeholder': 'USDOT Number', 'class': 'form-control input-md'}),
            'usdot_pin': forms.TextInput(attrs={'placeholder': 'USDOT PIN', 'class': 'form-control input-md upper'}),
            'txdmv': forms.TextInput(attrs={'placeholder': 'TXDMV Number', 'class': 'form-control input-md upper'}),
            'txdmv_user': forms.TextInput(attrs={'placeholder': 'TXDMV User', 'class': 'form-control input-md'}),
            'txdmv_passd': forms.TextInput(attrs={'placeholder': 'TXDMV Password', 'class': 'form-control input-md'}),
            'txdmv_date': forms.DateInput(attrs={'placeholder': 'TXDMV Date', 'class': 'form-control input-md'}),
            'txdmv_date_exp': forms.DateInput(attrs={'placeholder': 'Exp Date', 'class': 'form-control input-md'}),
            'mc': forms.TextInput(attrs={'placeholder': 'MC Number', 'class': 'form-control input-md'}),
            'mc_pin': forms.TextInput(attrs={'placeholder': 'MC PIN', 'class': 'form-control input-md'}),
            'boc3': forms.CheckboxInput(attrs={'data-off-color':"danger", 'class':"switch", 'data-size':"mini", 'data-on-text':"YES", 'data-off-text': "NO"}),
            'boc3_date': forms.DateInput(attrs={'placeholder': 'BOC3 Date', 'class': 'form-control input-md'}),
            'ucr': forms.CheckboxInput(attrs={'data-off-color':"danger", 'class':"switch", 'data-size':"mini", 'data-on-text':"YES", 'data-off-text': "NO"}),
            'ucr_date_exp': forms.DateInput(attrs={'placeholder': 'UCR Date', 'class': 'form-control input-md'}),
            'account_number': forms.TextInput(attrs={'placeholder': 'Account Number', 'class': 'form-control input-md'}),
            'account_user': forms.TextInput(attrs={'placeholder': 'Account User', 'class': 'form-control input-md'}),
            'account_password': forms.TextInput(attrs={'placeholder': 'Account Password', 'class': 'form-control input-md'}),
            'inter': forms.CheckboxInput(attrs={'id':"btninter", 'data-toggle':"toggle", 'type':"checkbox", 'data-on':"Inter-State", 'data-off':"Intra-State"}),
            'deactivate': forms.CheckboxInput(attrs={'data-off-color':"danger", 'class':"switch", 'data-size':"mini", 'data-on-text':"YES", 'data-off-text': "NO"}),
            'state': forms.Select(attrs={'class': 'form-control input-md'}, choices=(('Initiated', 'Initiated'), ('Pending', 'Pending'), ('Finalized', 'Finalized'))),
            'customers': forms.Select(attrs={'class': 'form-control input-md', 'required':'true', 'title':'Select one'}),
        }


class InsuranceForm(forms.ModelForm):

    class Meta:
        model = Insurance

        fields = [
            'down_payment',
            'policy_efective_date',
            'policy_date_exp',
            'policy_cargo_exp',
            'policy_physical_exp',
            'liability',
            'policy_liability',
            'cargo',
            'cargo_policy',
            'physical_damage',
            'physical_damg_policy',
            'other',
            'other_description',
            'other_policy',
            'policy_other_exp',
            'sale_type',
            'sale_date_fee',
            'total',
            'comision',
            'paid',
            'state',
            'customers',
            'paid_out',
            'balance_due',
            'monthlypay',
            'note',
        ]
        widgets = {
            'down_payment': forms.NumberInput(attrs={'placeholder': 'value Down', 'class': 'form-control input-md'}),
            'policy_efective_date': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md'}),
            'policy_date_exp': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md'}),
            'policy_cargo_exp': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md'}),
            'policy_physical_exp': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md'}),
            'liability': forms.NumberInput(attrs={'placeholder': 'value', 'class': 'form-control input-md'}),
            'policy_liability': forms.TextInput(attrs={'placeholder': 'policy number', 'class': 'form-control input-md upper'}),
            'cargo': forms.NumberInput(attrs={'placeholder': 'value', 'class': 'form-control input-md'}),
            'cargo_policy': forms.TextInput(attrs={'placeholder': 'policy number', 'class': 'form-control input-md upper'}),
            'physical_damage': forms.NumberInput(attrs={'placeholder': 'value', 'class': 'form-control input-md'}),
            'physical_damg_policy': forms.TextInput(attrs={'placeholder': 'policy number', 'class': 'form-control input-md upper'}),
            'policy_other_exp': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md'}),
            'other': forms.NumberInput(attrs={'placeholder': 'value', 'class': 'form-control input-md'}),
            'other_policy': forms.TextInput(attrs={'placeholder': 'policy number', 'class': 'form-control input-md upper'}),
            'other_description': forms.TextInput(attrs={'placeholder': 'Description', 'class': 'form-control input-md upper'}),
            'sale_type': forms.TextInput(attrs={'placeholder': 'type', 'class': 'form-control input-md upper'}),
            'sale_date_fee': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md'}),
            'total': forms.NumberInput(attrs={'placeholder': 'value', 'class': 'form-control input-md'}),
            'comision': forms.NumberInput(attrs={'placeholder': 'value', 'class': 'form-control input-md'}),
            'paid': forms.CheckboxInput(attrs={'data-off-color':"danger", 'class':"switch", 'data-size':"mini", 'data-on-text':"YES", 'data-off-text': "NO"}),
            'state': forms.Select(attrs={'class': 'form-control input-md'}, choices=(('Initiated', 'Initiated'), ('Pending', 'Pending'), ('Finalized', 'Finalized'))),
            'customers': forms.Select(attrs={'class': 'form-control input-md', 'required':'true', 'title':'Select one'}),
            'paid_out': forms.NumberInput(attrs={'placeholder': 'value', 'class': 'form-control input-md'}),
            'balance_due': forms.NumberInput(attrs={'placeholder': 'value', 'class': 'form-control input-md'}),
            'monthlypay': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md'}),
            'note': forms.Textarea(attrs={'class': 'form-control fee-value upper'}),
        }

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract


        fields = [
            'description',
            'serial',
            'start_date',
            'end_date',
            'type',
            'state',
            'customers',


        ]
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'State', 'class': 'form-control input-md'}),
            'serial': forms.TextInput(attrs={'placeholder': 'State', 'class': 'form-control input-md'}),
            'start_date': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md', 'required':'true', 'title':'Inset Start Date'}),
            'end_date': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md', 'required':'true', 'title':'Inset End Date'}),
            'type': forms.TextInput(attrs={'placeholder': 'State', 'class': 'form-control input-md'}),
            'state': forms.Select(attrs={'class': 'form-control input-md'}, choices=(
            ('Initiated', 'Initiated'), ('Pending', 'Pending'), ('Finalized', 'Finalized'))),
            'customers': forms.Select(
                attrs={'class': 'form-control input-md', 'required': 'true', 'title': 'Select one'}),
        }

class EquipmentForm(forms.ModelForm):

    class Meta:
        model = Equipment

        fields = [
            'customers',
            'state',
            'update',
            'type',
            'year',
            'model',
            'serial',
            'number',
            'plate_date_exp',
            'title_date_reg',
            'title_date_exp_reg',
            'title_date_insp',
            'title_date_exp_insp',
            'deactivate',

        ]
        widgets = {
            'customers': forms.Select(attrs={'class': 'form-control input-md','required': 'true', 'title': 'Select one'}),
            'state': forms.Select(attrs={'class': 'form-control input-md'}, choices=(('Initiated', 'Initiated'), ('Pending', 'Pending'), ('Finalized', 'Finalized'))),
            'type': forms.Select(attrs={'class': 'form-control input-md'}, choices=(('Truck', 'Truck'), ('Trailer', 'Trailer'), ('Other', 'Other'))),
            'year': forms.NumberInput(attrs={'placeholder': 'year', 'class': 'form-control input-md'}),
            'model': forms.TextInput(attrs={'placeholder': 'model', 'class': 'form-control input-md upper'}),
            'serial': forms.TextInput(attrs={'placeholder': 'serial number', 'class': 'form-control input-md upper','required': 'true', 'title': 'Insert Serial'}),
            'number': forms.TextInput(attrs={'placeholder': 'number', 'class': 'form-control input-md upper','required': 'true', 'title': 'Insert Number'}),
            'plate_date_exp': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md'}),
            'title_date_reg': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md'}),
            'title_date_exp_reg': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md'}),
            'title_date_insp': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md'}),
            'title_date_exp_insp': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md'}),
            'deactivate': forms.CheckboxInput(attrs={'data-off-color':"danger", 'class':"switch", 'data-size':"mini", 'data-on-text':"YES", 'data-off-text': "NO"}),
        }


class FileForm(forms.ModelForm):
    class Meta:
        model = File

        fields = [
            'name',
            'category',
            'url',

        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'name', 'class': 'form-control input-md upper'}),
            'category': forms.Select(attrs={'class': 'form-control input-md'}, choices=(('', '---------'),('Company', 'Company'),('Accidents', 'Accidents'), ('COI', 'COI'),('Insurance', 'Insurance'), ('Endorsments', 'Endorsments'), ('Misselenious', 'Misselenious'), ('Permit', 'Permit'), ('Quote', 'Quote'), ('Audit', 'Audit'), ('Contract', 'Contract'))),
            'url': forms.FileInput(),
        }

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver

        fields = [
            'customers',
            'name',
            'license_numb',
            'address',
            'dob',
            'lic_date_exp',
            'medicard_date_exp',
            'drugtest_date',
            'drugtest_date_exp',
            'mbr_date',
            'mbr_date_exp',
            'begining_date',
            'deactivate',
            'deactivate_date',
            'state',
        ]
        widgets = {
            'customers': forms.Select(attrs={'class': 'form-control input-md', 'required': 'true', 'title': 'Select one'}),
            'name': forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control input-md upper'}),
            'license_numb': forms.TextInput(attrs={'placeholder': 'License Number', 'class': 'form-control input-md upper'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control input-md upper'}),
            'dob': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md'}),
            'lic_date_exp': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md'}),
            'medicard_date_exp': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md'}),
            'drugtest_date': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md'}),
            'drugtest_date_exp': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md'}),
            'mbr_date': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md'}),
            'mbr_date_exp': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md'}),
            'begining_date': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md'}),
            'deactivate': forms.CheckboxInput(attrs={'data-off-color':"danger", 'class':"switch", 'data-size':"mini", 'data-on-text':"YES", 'data-off-text': "NO"}),
            'deactivate_date': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md'}),
            'state': forms.Select(attrs={'class': 'form-control input-md'}, choices=(
            ('Initiated', 'Initiated'), ('Pending', 'Pending'), ('Finalized', 'Finalized'))),
        }

class IftaForm(forms.ModelForm):
    class Meta:
        model = Ifta

        fields = [
            'customers',
            'type',
            'period',
            'nex_period',
            'paid',
            'payment_due',
            'state',
        ]
        widgets = {
            'customers': forms.Select(attrs={'class': 'form-control input-md', 'required': 'true', 'title': 'Select one'}),
            'type': forms.Select(attrs={'class': 'form-control input-md'}, choices=(('Anual', 'Anual'), ('Quarter', 'Quarter'))),
            'period': forms.Select(attrs={'class': 'form-control input-md'}, choices=(('Anual', 'Anual'), ('1st Quarter', '1st Quarter'), ('2nd Quarter', '2nd Quarter'), ('3rd Quarter', '3rd Quarter'), ('4th Quarter', '4th Quarter'))),
            'nex_period': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md'}),
            'paid': forms.CheckboxInput(
                attrs={'data-off-color': "danger", 'class': "switch", 'data-size': "mini", 'data-on-text': "YES",
                       'data-off-text': "NO"}),
            'payment_due': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md'}),
            'state': forms.Select(attrs={'class': 'form-control input-md'}, choices=(
            ('Initiated', 'Initiated'), ('Pending', 'Pending'), ('Finalized', 'Finalized'))),
        }

class AuditForm(forms.ModelForm):
    class Meta:
        model = Audit

        fields = [
            'customers',
            'contracts',
            'type',
            'auditor_name',
            'action_plan',
            'amount_paid',
            'date',
            'state',
            'results',
        ]
        widgets = {
            'customers': forms.Select(attrs={'class': 'form-control input-md', 'required': 'true', 'title': 'Select one'}),
            'contracts': forms.Select(attrs={'class': 'form-control input-md', 'required': 'true', 'title': 'Select one'}),
            'type': forms.TextInput(attrs={'placeholder': 'Type', 'class': 'form-control input-md upper'}),
            'auditor_name': forms.TextInput(attrs={'placeholder': 'Auditor Name', 'class': 'form-control input-md upper'}),
            'action_plan': forms.CheckboxInput(attrs={'data-off-color':"danger", 'class':"switch", 'data-size':"mini", 'data-on-text':"YES", 'data-off-text': "NO"}),
            'amount_paid': forms.NumberInput(attrs={'placeholder': 'value', 'class': 'form-control input-md'}),
            'date': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md'}),
            'state': forms.Select(attrs={'class': 'form-control input-md'}, choices=(
            ('Initiated', 'Initiated'), ('Pending', 'Pending'), ('Finalized', 'Finalized'))),
            'results': forms.TextInput(attrs={'placeholder': 'Results', 'class': 'form-control input-md upper'}),
        }

class EmailForm(forms.Form):
      topic = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-md upper topic', 'name':'topic'}), max_length=100)
      email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control input-md lower email', 'name':'email'}))
      message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control input-md upper sms', 'name':'sms'}))
      file = forms.FileField(widget=forms.FileInput(attrs={'class': 'file', 'name':'file'}),required=False)

      def clean_mensaje(self):
        sms = self.cleaned_data['message']
        num_word = len(sms.split())
        if num_word < 4:
            raise forms.ValidationError("Minimum 4 words are required!")
        return sms