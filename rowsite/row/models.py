from django.db import models

# Create your models here.
class Athlete(models.Model):
    name = models.CharField(max_length=50)
    side = models.CharField(max_length=20)
    year = models.CharField(max_length=20)
    height = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name
    
class Practice(models.Model):
    datetime = models.DateTimeField(auto_now=True)
    datetime.editable=True
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return str(self.datetime.date()) + " " +  self.name

class Result(models.Model):
    datetime = models.DateTimeField(auto_now=True)
    datetime.editable=True
    distance = models.IntegerField()
    time = models.IntegerField()
    type = models.CharField(max_length=20)
    athlete = models.ForeignKey(Athlete)
    practice = models.ForeignKey(Practice)

    def __unicode__(self):
        return str(self.datetime.date()) + " " + str(self.distance) + " " + str(self.time) + " " + self.type + " " + str(self.athlete)

class Weight(models.Model):
    datetime = models.DateTimeField(auto_now=True)
    datetime.editable=True
    athlete = models.ForeignKey(Athlete)
    weight = models.IntegerField()

    def __unicode__(self):
        return str(self.datetime.date()) + " " + str(self.athlete) + " " + str(self.weight)
