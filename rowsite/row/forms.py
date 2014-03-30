from django import forms
from datetime import datetime
from row.models import Athlete, Weight, Practice, Result

class AthleteForm(forms.ModelForm):
    name = forms.CharField(max_length=50, help_text="Your full name.", label="name")
    side = forms.CharField(max_length=20, help_text="Port, Starboard, Cox, Coach, or Other", label="side")
    year = forms.CharField(max_length=20, help_text="Fr, So, Jr, or Sr", label="year")
    height = forms.CharField(max_length=20, help_text="Your height in inches", label="height")

    class Meta:
        model = Athlete

class PracticeForm(forms.ModelForm):
	name = forms.CharField(max_length=20, help_text="What was the practice?", label="name")
	datetime = forms.DateTimeField(initial=datetime.now(), help_text="When was the practice? (Ex. 3/29/14 8:30)", label="datetime")

	# An inline class to provide additional information on the form.
	class Meta:
		# Provide an association between the ModelForm and a model
   		model = Practice
