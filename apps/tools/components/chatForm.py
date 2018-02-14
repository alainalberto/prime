from django import forms
from apps.tools.models import Chat


class chatForm(forms.ModelForm):
        class Meta:
            model = Chat

            fields = [
                'message',
            ]

            widgets = {
                'message': forms.TextInput(attrs={'placeholder': 'Message', 'class': 'form-control input-md'}),
            }