from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.
class Athlete(models.Model):
  
    side_choices = (
        ('Port', 'Port'),
        ('Starboard', 'Starboard'),
        ('Both', 'Both'),
        ('Coxswain', 'Coxswain'),
        ('Coach', 'Coach'),
        ('Other', 'Other')
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

    name = models.CharField(max_length=50)
    side = models.CharField(max_length=9, choices=side_choices)
    year = models.CharField(max_length=2, choices=year_choices, default='NA')
    status = models.CharField(max_length=20, choices=status_choices, default='Active')
    height = models.PositiveIntegerField()
    
    
    def __unicode__(self):
        return self.name
    
class Practice(models.Model):
    datetime = models.DateTimeField(editable=True)
    name = models.CharField(max_length=20)
    workout = models.CharField(max_length=20)

    workout_choices = (
        ('Erg', 'Erg'),
        ('Water', 'Water'),
        ('Bike', 'Bike')
    )

    def __unicode__(self):
        return str(self.datetime.date()) + " " +  self.name

class Result(models.Model):
    datetime = models.DateTimeField(editable=True)
    distance = models.IntegerField()
    time = models.IntegerField()
    athlete = models.ForeignKey(Athlete)
    practice = models.ForeignKey(Practice)

    def __unicode__(self):
        return str(self.datetime.date()) + " " + str(self.distance) + " " + str(self.time) + " " + str(self.athlete)

class Weight(models.Model):
    datetime = models.DateTimeField(editable=True)
    athlete = models.ForeignKey(Athlete)
    weight = models.DecimalField(decimal_places=1, max_digits=4)

    def __unicode__(self):
        return str(self.datetime.date()) + " " + str(self.athlete) + " " + str(self.weight)
