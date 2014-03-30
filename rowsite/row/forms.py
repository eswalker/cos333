from django import forms
from row.models import Athlete, Weight, Practice, Result

class AthleteForm(forms.ModelForm):
    name = forms.CharField(max_length=50, help_text="Your full name.")
    side = forms.CharField(max_length=20, help_text="Port, Starboard, Cox, Coach, or Other")
    year = forms.CharField(max_length=20, help_text="fr, so, jr, sr")
    name = forms.CharField(max_length=20, help_text="")


    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Athlete
