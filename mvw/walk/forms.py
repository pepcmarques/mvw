from django.forms import ModelForm
from django import forms

from .models import Walk

DISTANCE_CHOICES = list(range(1, 11))
MINUTE_CHOICES = list(range(1, 121))


class DateInput(forms.DateInput):
    input_type = 'date'


class WalkForm(ModelForm):
    class Meta:
        model = Walk
        fields = ["walkDate", "distance", "minutes"]
        labels = {
            'walkDate': 'Date or your walk',
            'distance': 'Rounded distance (Km)',
            'minutes': 'Walk duration (minutes)',
        }
        widgets = {
            "walkDate": DateInput(),
            "distance": forms.Select(choices=list(zip(DISTANCE_CHOICES, DISTANCE_CHOICES)), attrs={'class': 'form-control'}),
            "minutes": forms.Select(choices=list(zip(MINUTE_CHOICES, MINUTE_CHOICES)), attrs={'class': 'form-control'})
        }
