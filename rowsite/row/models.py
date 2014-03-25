from django.db import models

# Create your models here.
class Athlete(models.Model):
    name = models.CharField(max_length=50)
    side = models.CharField(max_length=20)
    year = models.CharField(max_length=20)
    height = models.CharField(max_length=20)
    

class Result(models.Model):
    datetime = models.DateTimeField(auto_now=True)
    distance = models.IntegerField()
    time = models.IntegerField()
    type = models.CharField(max_length=20)
    athlete = models.ForeignKey(Athlete)

class Weight(models.Model):
    datetime = models.DateTimeField(auto_now=True)
    weight = models.IntegerField()
