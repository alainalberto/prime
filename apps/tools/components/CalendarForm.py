from django import forms
from apps.tools.models import Calendar


class CalendarForm(forms.ModelForm):
    class Meta:
        model = Calendar

        fields = [
            'id',
            'title',
            'color',
            'allDay',
            'start',
            'startTimer',
            'end',
            'endTimer',
        ]
        labels = {
            'title': 'Title to Events:',
            'color': 'Category:',
            'allDay': 'is All day:',
            'start': 'Start Date:',
            'startTimer': 'Start Timer:',
            'end': 'End Date:',
            'endTimer': 'End Timer',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title', 'class': 'form-control input-md'}),
            'color': forms.Select(attrs={'class': 'form-control input-md'}, choices=(('#E74C3C','Very Importan'), ('#DC7633', 'Importan'), ('#27AE60', 'Event'))),
            'allDay': forms.CheckboxInput(attrs={'data-off-color':"danger", 'class':"switch", 'data-size':"mini", 'data-on-text':"YES", 'data-off-text': "NO"}),
            'start': forms.DateInput(attrs={'class': 'form-control input-md'}),
            'startTimer': forms.TimeInput(attrs={'class': 'form-control'}),
            'end': forms.DateInput(attrs={'class': 'form-control input-md'}),
            'endTimer': forms.TimeInput(attrs={'class': 'form-control'}),
        }