from django import forms
from django.forms import ModelForm
from .models import Event

class Create_Event(ModelForm):
    """Class used to receive user input from form and create model object in database"""
    class Meta:
        model = Event
        fields = '__all__'

    #override clean function to check start time is greater than end time
    def clean(self):
        cleaned_data = super().clean()
        if len(cleaned_data)==4:
            start = cleaned_data['start']
            end = cleaned_data['end']
            if start!=None and end!=None:
                if start>end:
                    raise forms.ValidationError('The start time must be less than the end time.')
                    return cleaned_data
