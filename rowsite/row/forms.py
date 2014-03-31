from django import forms
from datetime import datetime
from row.models import Athlete, Weight, Practice, Result

class AthleteForm(forms.ModelForm):
    name = forms.CharField(max_length=50, help_text="Your full name.", label="name")
    side = forms.ChoiceField(choices=Athlete.side_choices, help_text="Port, Starboard, Coxswain, Coach, or Other", label="side")
    year = forms.ChoiceField(choices=Athlete.year_choices, help_text="Fr, So, Jr, or Sr", label="year")
    height = forms.IntegerField(min_value=0, help_text="Your height in inches", label="height")

    def clean_height(self):
        height = self.cleaned_data["height"]
        if height > 100 or height < 30:
            raise forms.ValidationError('Height must be between 30 and 100 inches.')
        return height

    class Meta:
        model = Athlete

class PracticeForm(forms.ModelForm):
	name = forms.CharField(max_length=20, help_text="What was the practice?", label="name")
	datetime = forms.DateTimeField(initial=datetime.now(), help_text="When was the practice? (Ex. 3/29/14 8:30)", label="datetime")
	workout = forms.ChoiceField(max_length=20, help_text="Erg, Water, Bike, etc.", label="type")
    
    # An inline class to provide additional information on the form.
	class Meta:
		# Provide an association between the ModelForm and a model
   		model = Practice

class WeightForm(forms.ModelForm):
    athlete = forms.ModelChoiceField(queryset=Athlete.objects.all(), help_text="Choose an athlete", label="athlete")
    weight = forms.DecimalField(help_text="Weight in lbs", decimal_places=1, label="weight")
    datetime = forms.DateTimeField(initial=datetime.now(), help_text="When was the weigh-in? (Ex. 3/29/14 8:30)", label="datetime")

    def clean_weight(self):
        weight = self.cleaned_data["weight"]
        if weight > 400 or weight < 50:
            raise forms.ValidationError('Weight must be between 50 and 400 lbs.')
        return weight

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Weight

class ResultForm(forms.ModelForm):
    datetime = forms.DateTimeField(initial=datetime.now(), help_text="When was the practice? (Ex. 3/29/14 8:30)", label="datetime")
    distance = forms.IntegerField(help_text="Distance", label="distance")
    time = forms.IntegerField(help_text="Time (in seconds)", label="time")
    athlete = forms.ModelChoiceField(queryset=Athlete.objects.all(), help_text="Choose an athlete", label="athlete")
    practice = forms.ModelChoiceField(queryset=Practice.objects.all(), help_text="Choose a practice", label="practice")


     # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Result