from django import forms
from row.models import Athlete, Weight, Practice, Result

class AthleteForm(forms.ModelForm):
    name = forms.CharField(max_length=50, help_text="Your full name.")
    side = forms.CharField(max_length=20, help_text="Port, Starboard, Cox, Coach, or Other")
    year = forms.CharField(max_length=20, help_text="Fr, So, Jr, or Sr")
    height = forms.CharField(max_length=20, help_text="Your height in inches")

    class Meta:
        model = Athlete
