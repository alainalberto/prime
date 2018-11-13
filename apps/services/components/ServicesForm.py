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
            'paid_out',
            'balance_due',
            'monthlypay',
            'note',
            'months',
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
            'paid_out': forms.NumberInput(attrs={'placeholder': 'value', 'class': 'form-control input-md'}),
            'balance_due': forms.NumberInput(attrs={'placeholder': 'value', 'class': 'form-control input-md'}),
            'monthlypay': forms.NumberInput(attrs={'placeholder': 'Number of day', 'class': 'form-control input-md'}),
            'note': forms.Textarea(attrs={'class': 'form-control fee-value upper'}),
            'monthls': forms.NumberInput(attrs={'placeholder': 'Many Month', 'class': 'form-control input-md'}),
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


        ]
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'State', 'class': 'form-control input-md'}),
            'serial': forms.TextInput(attrs={'placeholder': 'State', 'class': 'form-control input-md'}),
            'start_date': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md', 'required':'true', 'title':'Inset Start Date'}),
            'end_date': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md', 'required':'true', 'title':'Inset End Date'}),
            'type': forms.TextInput(attrs={'placeholder': 'State', 'class': 'form-control input-md'}),
            'state': forms.Select(attrs={'class': 'form-control input-md'}, choices=(
                ('Initiated', 'Initiated'), ('Pending', 'Pending'), ('Finalized', 'Finalized'))),
        }

class EquipmentForm(forms.ModelForm):

    class Meta:
        model = Equipment

        fields = [
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
            'category': forms.Select(attrs={'class': 'form-control input-md'}, choices=(('', '---------'),('Company', 'Company'),('Accidents', 'Accidents'), ('COI', 'COI'),('Insurance', 'Insurance'), ('Endorsments', 'Endorsements'), ('Misselenious', 'Miscellameous'), ('Permit', 'Permit'), ('Quote', 'Quote'), ('Audit', 'Audit'), ('Contract', 'Contract'), ('Accounting', 'Accounting'), ('ID_Card', 'ID Card'), ('Binders_&_Confirmation', 'Binders & Confirmation'), ('Bor', 'Bor'), ('Client_Proposals', 'Client Proposals'), ('Correspondece', 'Correspondece'), ('Exposure_Data_&_Marketing', 'Exposure Data & Marketing'), ('Licenses_&_Permits', 'Licenses & Permits'), ('Policies', 'Policies'))),
            'url': forms.FileInput(),
        }

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver

        fields = [
            'name',
            'license_numb',
            'address',
            'phone',
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
            'name': forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control input-md upper'}),
            'license_numb': forms.TextInput(attrs={'placeholder': 'License Number', 'class': 'form-control input-md upper'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control input-md upper'}),
            'phone': forms.NumberInput(attrs={'placeholder': 'Phone Number', 'class': 'form-control input-md'}),
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
            'type',
            'period',
            'nex_period',
            'paid',
            'payment_due',
            'state',
        ]
        widgets = {
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

class CompanesDispatchForm(forms.ModelForm):
    class Meta:
        model = DispatchLoad

        fields = [
            'biller',
            'biller_address',
            'biller_email',
            'start_date',
            'waytopay',
            'discount',
            'paid',
            'prefix',
            'end_date',
            'subtotal',
            'total',
            'comission_fee',
            'wire_fee',
            'ach_fee',

        ]
        labels = {
            'start_date': 'Start Date:',
            'waytopay': 'Payment Method:',
            'discount': 'Discount:',
            'paid': 'Paid:',
            'prefix': 'Prefix:',
            'end_date': 'End Date:',
            'subtotal': 'Subtotal:',
            'total': 'Total:',
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'placeholder': 'Start Date', 'class': 'form-control input-md', 'readonly': ''}),
            'waytopay': forms.Select(attrs={'class': 'form-control input-md'}, choices=(
                ('Cash', 'Cash'), ('Check', 'Check'), ('Credit Card', 'Credit Card'))),
            'paid': forms.CheckboxInput(
                attrs={'data-off-color': "danger", 'class': "switch", 'data-size': "mini", 'data-on-text': "YES",
                       'data-off-text': "NO"}),
            'prefix': forms.TextInput(attrs={'placeholder': 'Prefix', 'class': 'form-control input-md upper'}),
            'end_date': forms.DateInput(attrs={'placeholder': 'End Date', 'class': 'form-control input-md', 'readonly': ''}),
            'discount': forms.NumberInput(attrs={'placeholder': '0.00', 'class': 'form-control discount fee'}),
            'subtotal': forms.NumberInput(
                attrs={'placeholder': '0.00', 'class': 'form-control servSutotal', 'readonly': ''}),
            'total': forms.NumberInput(
                attrs={'placeholder': '0.00', 'class': 'form-control serviTotal', 'readonly': ''}),
            'comission_fee': forms.NumberInput(
                attrs={'placeholder': '0.00', 'class': 'form-control comission fee'}),
            'wire_fee': forms.NumberInput(attrs={'placeholder': '0.00', 'class': 'form-control wire fee'}),
            'ach_fee': forms.NumberInput(attrs={'placeholder': '0.00', 'class': 'form-control ach fee'}),

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


class CustomerAplicForm(forms.ModelForm):
    class Meta:
        model = CustomerAplic

        fields = [
            'fullname',
            'company_name',
            'address',
            'phone',
            'email',
            'usdot',
            'mc',
            'txdmv',
        ]

        widgets = {
            'fullname' : forms.TextInput(attrs={'class': 'form-control upper', 'name': 'fullname', 'required':'true'}),
            'company_name' : forms.TextInput(attrs={'class': 'form-control upper', 'name': 'company_name'}),
            'address' : forms.TextInput(attrs={'class': 'form-control upper', 'name': 'address'}),
            'phone' : forms.NumberInput(attrs={'class': 'form-control phone', 'name': 'pone', 'required':'true'}),
            'email' : forms.EmailInput(attrs={'class': 'form-control lower email', 'name': 'email', 'required':'true'}),
            'usdot' : forms.TextInput(attrs={'class': 'form-control input-md upper', 'name': 'usdot'}),
            'mc' : forms.TextInput(attrs={'class': 'form-control input-md upper', 'name': 'mc'}),
            'txdmv' : forms.TextInput(attrs={'class': 'form-control input-md upper', 'name': 'txdmv'}),
        }



class PaymentInfoForm(forms.ModelForm):
    class Meta:
        model = PaymentInfo

        fields = [
            'namecard',
            'credicard',
            'securitycode',
            'expdate',
        ]

        widgets = {
            'namecard' : forms.TextInput(attrs={'class': 'form-control input-md upper', 'name': 'namecard', 'required':'true'}),
            'credicard' : forms.NumberInput(attrs={'class': 'form-control input-md', 'name': 'credicard', 'required':'true'}),
            'securitycode' : forms.PasswordInput(attrs={'class': 'form-control input-md code', 'name': 'securitycode', 'required':'true'}),
            'expdate' : forms.TextInput(attrs={'class': 'form-control input-md date', 'name': 'expdate', 'required':'true'}),

        }




class NewCompanyForm(forms.ModelForm):

    class Meta:
        model = NewCompany

        fields = [
            'name1',
            'name2',
            'name3',
            'licdriver',
        ]

        widgets = {
            'name1' : forms.TextInput(attrs={'class': 'form-control input-md upper', 'name': 'name1', 'required':'true'}),
            'name2' : forms.TextInput(attrs={'class': 'form-control input-md upper', 'name': 'name2', 'required':'true'}),
            'name3' : forms.TextInput(attrs={'class': 'form-control input-md upper', 'name': 'name3', 'required':'true'}),
            'licdriver' : forms.TextInput(attrs={'class': 'form-control input-md upper', 'name': 'licedriver', 'required':'true'}),

        }



class IftaAplicForm(forms.ModelForm):
    class Meta:
        model = IftaAplic

        fields = [
            'rtcode',
            'namebank',
            'rootingnumb',
            'accountnumb',
        ]

        widgets = {
            'rtcode': forms.TextInput(attrs={'class': 'form-control input-md upper', 'name': 'rtcode'}),
            'namebank' : forms.TextInput(attrs={'class': 'form-control input-md upper', 'name': 'namebank', 'required':'true'}),
            'rootingnumb' : forms.NumberInput(attrs={'class': 'form-control input-md number', 'name': 'rootingnumb', 'required':'true'}),
            'accountnumb' : forms.NumberInput(attrs={'class': 'form-control input-md number', 'name': 'accountnumb', 'required':'true'}),

        }



class DispatchAplicForm(forms.ModelForm):
    class Meta:
        model = DispatchAplic

        fields = [
            'flatbead',
            'van',
            'refer',
            'other',
            'otherdescrp',
        ]
        widgets = {
            'flatbead' : forms.CheckboxInput(attrs={'class': 'form-control input-md checkbox', 'name': 'flatbead'}),
            'van': forms.CheckboxInput(attrs={'class': 'form-control input-md checkbox', 'name': 'van'}),
            'refer': forms.CheckboxInput(attrs={'class': 'form-control input-md checkbox', 'name': 'refer'}),
            'other':forms.CheckboxInput(attrs={'class': 'form-control input-md checkbox', 'name': 'other'}),
            'otherdescrp':forms.TextInput(attrs={'class': 'form-control input-md descrp', 'name': 'otherdescrp'}),

        }




class AuditAplicForm(forms.ModelForm):

    class Meta:
        model = AuditAplic

        fields = [
            'usdotpin',
            'usdotnumb',
            'drivernumb',
            'unitnumb',
            'auditormane',
            'auditaddress',
            'date',
        ]
        widgets = {
            'usdotpin':forms.TextInput(attrs={'class': 'form-control input-md upper', 'name': 'usdotpin'}),
            'usdotnumb':forms.TextInput(attrs={'class': 'form-control input-md upper', 'name': 'usdotnumb'}),
            'drivernumb':forms.TextInput(attrs={'class': 'form-control input-md upper', 'name': 'drivernumb'}),
            'unitnumb':forms.TextInput(attrs={'class': 'form-control input-md upper', 'name': 'unitnumb'}),
            'auditormane':forms.TextInput(attrs={'class': 'form-control input-md upper', 'name': 'auditormane'}),
            'auditaddress':forms.TextInput(attrs={'class': 'form-control input-md upper', 'name': 'auditaddress'}),
            'date':forms.DateTimeInput(attrs={'class': 'form-control input-md', 'name': 'date'}),

        }




class ApportionedAplicForm(forms.ModelForm):
    class Meta:
        model = ApportionedAplic
        fields = [
            'companyein',
            'unitnumb',
            'vin',
            'irpacount',
        ]

        widgets = {
            'companyein':forms.TextInput(attrs={'class': 'form-control input-md upper', 'name': 'companyein', 'required':'true'}),
            'unitnumb':forms.TextInput(attrs={'class': 'form-control input-md upper', 'name': 'unitnumb'}),
            'vin':forms.TextInput(attrs={'class': 'form-control input-md upper', 'name': 'vin'}),
            'irpacount':forms.TextInput(attrs={'class': 'form-control input-md upper', 'name': 'irpacount'}),

        }




class DriverAplicForm(forms.ModelForm):
    class Meta:
        model = DriverAplic

        fields = [
            'name',
            'license_numb',
            'experience',
            'dob',
            'lic_date_exp',
        ]

        widgets = {
            'name':forms.TextInput(attrs={'class': 'form-control input-md upper', 'name': 'name'}),
            'license_numb':forms.TextInput(attrs={'class': 'form-control input-md upper', 'name': 'license_numb'}),
            'experience':forms.NumberInput(attrs={'class': 'form-control input-md', 'name': 'experience'}),
            'dob':forms.TextInput(attrs={'class': 'form-control input-md upper ', 'name': 'dob'}),
            'lic_date_exp':forms.DateInput(attrs={'class': 'form-control input-md ', 'name': 'lic_date_exp'}),

        }





class VehicleAplicForm(forms.ModelForm):

    class Meta:
        model = VehicleAplic
        fields = [
            'type',
            'year',
            'marke',
            'vin',
            'owned',
            'leased',

        ]

        widgets = {
            'type':forms.TextInput(attrs={'class': 'form-control input-md upper', 'name': 'type'}),
            'year':forms.TextInput(attrs={'class': 'form-control input-md upper', 'name': 'year'}),
            'marke':forms.TextInput(attrs={'class': 'form-control input-md upper', 'name': 'marke'}),
            'vin':forms.TextInput(attrs={'class': 'form-control input-md upper', 'name': 'vin'}),
            'owned':forms.CheckboxInput(attrs={'class': 'form-control input-md checkbox', 'name': 'owned'}),
            'leased':forms.CheckboxInput(attrs={'class': 'form-control input-md checkbox', 'leased': 'namebank'}),

        }
