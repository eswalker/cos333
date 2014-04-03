from django import forms
from datetime import datetime
from row.models import Athlete, Weight, Practice, Result, Boat, Lineup
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_password(self):
        password = self.cleaned_data["password"]
        if len(password) < 8:
            raise forms.ValidationError('Password is too short')
        if password.lower() == password or password.upper() == password:
            raise forms.ValidationError('Password must have lower and uppercase letters')
        return password

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'password')

class AthleteForm(forms.ModelForm):
    name = forms.CharField(max_length=50, help_text="Your full name.", label="name")
    side = forms.ChoiceField(choices=Athlete.side_choices, help_text="Port, Starboard, Coxswain, Coach, or Other", label="side")
    year = forms.ChoiceField(choices=Athlete.year_choices, help_text="Fr, So, Jr, or Sr", label="year")
    height = forms.IntegerField(min_value=0, help_text="Your height in inches", label="height")
    status = forms.ChoiceField(choices=Athlete.status_choices, help_text="Athlete status (Active, Injured, or Retired).", label="status")

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
	workout = forms.ChoiceField(choices=Practice.workout_choices, help_text="Erg, Water, Bike, etc.", label="type")
    
	class Meta:
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

    class Meta:
        model = Weight

class ResultForm(forms.ModelForm):
    datetime = forms.DateTimeField(initial=datetime.now(), help_text="When was the practice? (Ex. 3/29/14 8:30)", label="datetime")
    distance = forms.IntegerField(help_text="Distance", label="distance")
    time = forms.IntegerField(help_text="Time (in seconds)", label="time")
    athlete = forms.ModelChoiceField(queryset=Athlete.objects.all(), help_text="Choose an athlete", label="athlete")
    practice = forms.ModelChoiceField(queryset=Practice.objects.all(), help_text="Choose a practice", label="practice")

    class Meta:
        model = Result

class BoatForm(forms.ModelForm):
    name = forms.CharField(max_length=20, help_text="What is the boat's name?", label="name")
    seats = forms.ChoiceField(choices=Boat.seats_choices, help_text="How many seats are there in the boat?")
    coxed = forms.ChoiceField(choices=Boat.coxed_choices, help_text="Does the boat have a coxswain?")

    class Meta:
        model = Boat

class LineupForm(forms.ModelForm):
    practice = forms.ModelChoiceField(queryset=Practice.objects.all(), help_text="Choose a practice", label="practice")
    boat = forms.ModelChoiceField(queryset=Boat.objects.all(), help_text="Choose a boat", label="boat")
    position = forms.ChoiceField(choices=Lineup.position_choices, help_text="Identify the lineup", label="position")
    athletes = forms.CharField(max_length=200, help_text="Who are the athletes?")

    class Meta:
        model = Lineup