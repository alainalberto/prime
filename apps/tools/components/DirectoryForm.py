from django import forms
from apps.tools.models import *
from django.contrib.auth.models import User, Group
from django.db.models.query_utils import DeferredAttribute


class DirectoryForm(forms.ModelForm):
    class Meta:
        model = Directory

        fields = [
            'name',
            'phone',
            'email',
            'address',
        ]
        labels = {
            'name': 'Name:',
            'phone': 'Phone:',
            'email': 'Email:',
            'address': 'Address:',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control input-md'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone', 'class': 'form-control input-md'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control input-md'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control input-md'}),
        }