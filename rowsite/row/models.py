from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from django.core.mail import send_mail

import datetime
import time

'''
class Team(models.Model):
    name = models.CharField(max_length=50)
    head_coach = models.OneToOneField(User)

    def __unicode__(self):
        return self.name
'''

class Invite(models.Model):
    #team = models.ForeignKey(Team)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    email = models.EmailField()
    invite_key = models.CharField(max_length=50)
    used = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)
    
    role_choices = (
        ('Rower', 'Rower'),
        ('Coxswain', 'Coxswain'),
        ('Coach', 'Coach'),
        ('Observer', 'Observer')
    )

    role = models.CharField(max_length=20, choices=role_choices)

    def is_recent(self):
        today = datetime.datetime.today()
        today_unix_timestamp = time.mktime(today.timetuple())
        created_unix_timestamp = time.mktime(self.created_at.timetuple())

        delta = today_unix_timestamp - created_unix_timestamp
        return delta < ( 7 * 3600 * 24)

    def send_invite(self):
        link = "https://cos333.herokuapp.com/invited/" + self.invite_key + "/"
        recipients = []
        recipients.append(self.email)
        sender = "VirtualBoathouse@gmail.com"
        subject = "Invitation to join Virtual Boathouse for Princeton Lightweight Crew"
        message = 'We\'re working on a rowing web application as part of our COS 333 project and would like you to take a look. Please go to ' + link + ' to register.\n\nPlease contact any of us with any questions or concerns.\n\nThanks!\n\nEd Walker, Brian Rosenfeld, Matt Drabick, Sam Jordan'
        
        send_mail(subject, message, sender, recipients, fail_silently=False)

    def __unicode__(self):
        return self.role + " " + self.email

# Create your models here.
class Athlete(models.Model):  
    side_choices = (
        ('Port', 'Port'),
        ('Starboard', 'Starboard'),
        ('Both', 'Both'),
        ('NA', 'Not Applicable')
    )
    year_choices = (
        ('Fr', 'Freshman'),
        ("So", 'Sophomore'),
        ('Jr', 'Junior'),
        ('Sr', 'Senior'),
        ('NA', 'Not Applicable')
    )

    status_choices = (
        ('Active', 'Active'),
        ('Injured', 'Injured'),
        ('Retired', 'Retired')
    )

    user = models.OneToOneField(User)
    name = models.CharField(max_length=50)
    side = models.CharField(max_length=9, choices=side_choices)
    role = models.CharField(max_length=20, choices=Invite.role_choices)
    year = models.CharField(max_length=2, choices=year_choices, default='NA')
    status = models.CharField(max_length=20, choices=status_choices, default='Active')
    height = models.PositiveIntegerField()
    api_key = models.CharField(max_length=50)
    
    def is_leader(self):
        return self.role == "Coach" or self.role == "Coxswain"
    
    def __unicode__(self):
        return self.name

class Practice(models.Model):
    datetime = models.DateTimeField(editable=True)
    name = models.CharField(max_length=20)
    workout = models.CharField(max_length=20)

    workout_choices = (
        ('Erg', 'Erg'),
        ('Water', 'Water'),
    )

    def __unicode__(self):
        return str(self.datetime.date()) + " " +  self.name

class Piece(models.Model):
    datetime = models.DateTimeField(editable=True)
    name = models.CharField(max_length=20)
    practice = models.ForeignKey(Practice)

    def __unicode__(self):
        return str(self.datetime.date()) + " " +  self.name

class Result(models.Model):
    datetime = models.DateTimeField(editable=True)
    distance = models.PositiveIntegerField()
    time = models.IntegerField()
    athlete = models.ForeignKey(Athlete)
    piece = models.ForeignKey(Piece)

    def __unicode__(self):
        return str(self.datetime.date()) + " " + str(self.distance) + " " + str(self.time) + " " + str(self.athlete)

class Weight(models.Model):
    datetime = models.DateTimeField(editable=True)
    athlete = models.ForeignKey(Athlete)
    weight = models.DecimalField(decimal_places=1, max_digits=4)

    def __unicode__(self):
        return str(self.datetime.date()) + " " + str(self.athlete) + " " + str(self.weight)

class Boat(models.Model):

    seats_choices = (
        (1, 1),
        (2, 2),
        (4, 4),
        (8, 8),
    )

    coxed_choices = (
        (True, "Yes"),
        (False, "No"),
    )

    name = models.CharField(max_length=20)
    seats = models.PositiveIntegerField(choices=seats_choices)
    coxed = models.BooleanField(choices=coxed_choices)

    def __unicode__(self):
        return self.name

class Lineup(models.Model):
    position_choices = (
        ('1V', '1V'),
        ('2V', '2V'),
        ('3V', '3V'),
        ('4V', '4V'),
        ('5V', '5V'),
        ('1F', '1F'),
        ('2F', '2F'),
        ('Mixed', 'Mixed'),
    )

    piece = models.ForeignKey(Piece)
    boat = models.ForeignKey(Boat)
    position = models.CharField(max_length=10, choices=position_choices)
    athletes = models.ManyToManyField(Athlete, through='Seat')

    def __unicode__(self):
        return self.position + " " + str(self.boat)

    def getAthletes(self):
        print str(self.athletes.all())
        print str(self.athletes.all().order_by('seat__number'))
        return self.athletes.all().order_by('seat__number')

class Seat(models.Model):
    athlete = models.ForeignKey(Athlete)
    lineup = models.ForeignKey(Lineup)
    number = models.PositiveIntegerField()

class Note(models.Model):
    subject = models.CharField(max_length=50)
    piece = models.ForeignKey(Piece, null=True)
    practice = models.ForeignKey(Practice, null=True)
    author = models.ForeignKey(Athlete)
    note = models.TextField()

    def __unicode__(self):
        return self.subject
