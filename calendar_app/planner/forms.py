from django import forms
from django.forms import ModelForm
from .models import Event


class Create_Event(ModelForm):
    """Class used to receive user input from form and create model object in database"""
    class Meta:
        model = Event
        fields = '__all__'

    #override clean function to do error handling for start time less than end time
    #and if overlap in existing events
    def clean(self):
        cleaned_data = super().clean()
        if len(cleaned_data)==4:
            start = cleaned_data['start']
            end = cleaned_data['end']
            day = cleaned_data['day']
            if start!=None and end!=None:
                if start>end:
                    raise forms.ValidationError("Error")
            return cleaned_data
