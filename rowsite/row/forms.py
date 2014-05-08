from django import forms
from datetime import datetime
from row.models import Athlete, Weight, Practice, Piece, Result, Boat, Lineup, Note, Invite
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Must contain at least 6 characters and both upper and lowercase letters.")

    def clean_password(self):
        password = self.cleaned_data["password"]
        if len(password) < 6:
            raise forms.ValidationError('Password is too short')
        if password.lower() == password or password.upper() == password:
            raise forms.ValidationError('Password must have lower and uppercase letters')
        return password

    class Meta:
        model = User
        fields = ('password',)

class UserLoginForm(forms.ModelForm):
    username = forms.CharField(max_length=75, help_text="", label="Email")
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")
    class Meta:
        model = User
        fields = ('username', 'password')

class UserPasswordChangeForm(PasswordChangeForm):
    def clean_new_password1(self):
        password = self.cleaned_data["new_password1"]
        if len(password) < 6:
            raise forms.ValidationError('Password is too short')
        if password.lower() == password or password.upper() == password:
            raise forms.ValidationError('Password must have lower and uppercase letters')
        return password

class InviteForm(forms.ModelForm):
    email = forms.EmailField(label="Email")
    role = forms.ChoiceField(choices=Invite.role_choices, help_text="Rower, Coxswain, Coach, or Observer", label="Role")

    class Meta:
        model = Invite
        fields = ('email', 'role')

class AthleteForm(forms.ModelForm):
    name = forms.CharField(max_length=50, help_text="Your full name.", label="Name")
    side = forms.ChoiceField(choices=Athlete.side_choices, help_text="Port, Starboard, Coxswain, Coach, or Other", label="Side")
    year = forms.ChoiceField(choices=Athlete.year_choices, help_text="Fr, So, Jr, or Sr", label="Year")
    height = forms.IntegerField(min_value=0, help_text="Your height in inches", label="Height")
    status = forms.ChoiceField(choices=Athlete.status_choices, help_text="Athlete status (Active, Injured, or Retired).", label="Status")

    def clean_height(self):
        height = self.cleaned_data["height"]
        if height > 100 or height < 30:
            raise forms.ValidationError('Height must be between 30 and 100 inches.')
        return height

    def clean_name(self):
        return self.cleaned_data["name"].rstrip()

    class Meta:
        model = Athlete
        fields = ('name', 'side', 'year', 'height', 'status')

class PracticeForm(forms.ModelForm):
	name = forms.CharField(max_length=20, help_text="What was the practice?", label="Name")
	datetime = forms.DateTimeField(initial=datetime.now(), help_text="When was the practice? (Ex. 3/29/14 8:30)", label="Datetime")
	workout = forms.ChoiceField(widget=forms.HiddenInput(), choices=Practice.workout_choices, help_text="Erg or Water", label="Type")
    
	class Meta:
   		model = Practice

class PieceForm(forms.ModelForm):
    name = forms.CharField(max_length=20, help_text="What was the piece?", label="Name")
    datetime = forms.DateTimeField(initial=datetime.now(), help_text="When was the practice? (Ex. 3/29/14 8:30)", label="Datetime")
    practice = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=Practice.objects.all(), help_text="Choose a practice", label="Practice")

    class Meta:
        model = Piece

class WeightForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user_athlete = kwargs.pop("user_athlete")
        super(WeightForm, self).__init__(*args, **kwargs)

    athlete = forms.ModelChoiceField(queryset=Athlete.objects.all().exclude(name="COACH").order_by('name'), help_text="Choose an athlete", label="Athlete")
    weight = forms.DecimalField(help_text="Weight in lbs", decimal_places=1, label="Weight")
    datetime = forms.DateTimeField(initial=datetime.now(), help_text="When was the weigh-in? (Ex. 3/29/14 8:30)", label="Datetime")

    def clean_weight(self):
        weight = self.cleaned_data["weight"]
        if weight > 400 or weight < 50:
            raise forms.ValidationError('Weight must be between 50 and 400 lbs.')
        return weight

    def clean_athlete(self):
        athlete = self.cleaned_data["athlete"]
        if self.user_athlete.role == "Coxswain" or self.user_athlete.role =="Coach": return athlete
        if athlete != self.user_athlete:
            raise forms.ValidationError("You do not have permission to edit this athlete's weight.")
        return athlete

    class Meta:
        model = Weight

class ResultForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.athlete2 = kwargs.pop("athlete2")
        super(ResultForm, self).__init__(*args, **kwargs)

    def clean_time(self):
        time = self.cleaned_data["time"]
        return time * 1000

    datetime = forms.DateTimeField(initial=datetime.now(), help_text="When was the practice? (Ex. 3/29/14 8:30)", label="Datetime")
    distance = forms.IntegerField(help_text="Distance", label="Distance")
    time = forms.IntegerField(help_text="Time (in seconds)", label="Time")
    athlete = forms.ModelChoiceField(queryset=Athlete.objects.all().exclude(name="COACH").order_by('name'), help_text="Choose an athlete", label="Athlete")
    piece = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=Piece.objects.all(), help_text="Choose a piece", label="Piece")

    class Meta:
        model = Result

    def clean_distance(self):
        distance = self.cleaned_data["distance"]
        if distance <= 0:
            raise forms.ValidationError('Distance must be positive.')
        return distance

    def clean_athlete(self):
        athlete = self.cleaned_data["athlete"]
        if self.athlete2.role == "Coxswain" or self.athlete2.role =="Coach": return athlete
        if athlete != self.athlete2:
            raise forms.ValidationError("You do not have permission to edit this athlete's result.")
        return athlete

class BoatForm(forms.ModelForm):
    name = forms.CharField(max_length=20, help_text="What is the boat's name?", label="Name")
    seats = forms.ChoiceField(choices=Boat.seats_choices, help_text="How many seats are there in the boat?", label="Seats")
    coxed = forms.ChoiceField(choices=Boat.coxed_choices, help_text="Does the boat have a coxswain?", label="Coxed")

    class Meta:
        model = Boat

class LineupForm(forms.ModelForm):
    piece = forms.ModelChoiceField(queryset=Piece.objects.filter(practice__workout="Water"), help_text="Choose a piece", label="Piece")
    boat = forms.ModelChoiceField(queryset=Boat.objects.all(), help_text="Choose a boat", label="Boat")
    position = forms.ChoiceField(choices=Lineup.position_choices, help_text="Identify the lineup", label="Position")
    athletes = forms.ModelMultipleChoiceField(queryset=Athlete.objects.order_by('name'), widget=forms.SelectMultiple, help_text="Who are the athletes?", label="Athletes")

    def clean_athletes(self):
        boat = self.cleaned_data["boat"]
        seats = boat.seats
        coxed = boat.coxed

        athletes = self.cleaned_data["athletes"]
        num_athletes = len(athletes)

        if num_athletes != seats + coxed:
            error = "There should be "
           
            if seats == 1: error = error + "1 rower"
            else: error = error + str(seats) + " rowers"
           
            if coxed == True: error = error + " and a coxswain"

            error = error + " in this boat. You have entered " + str(num_athletes)
            error = error + (" athlete." if num_athletes == 1 else " athletes.")

            raise forms.ValidationError(error)

        return athletes

    def clean_piece(self):
        piece = self.cleaned_data["piece"]
        workout = piece.practice.workout

        if workout == "Erg":
            raise forms.ValidationError("You cannot add a lineup to an erg piece.")
        return piece

    class Meta:
        model = Lineup

class NoteForm(forms.ModelForm):
    subject = forms.CharField(max_length=50, help_text="50 characters or fewer", label='Subject')

    class Meta:
        model = Note
        fields = ('subject', 'note')