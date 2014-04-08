from row.models import Athlete
import sys

old = Athlete.objects.all()
for item in old:
	old.delete()

f = open("rowers")

# name,side,year,status,height 
for line in f:
	fields = line.split(", ")
	athlete = Athlete(name=fields[0], side=fields[1], year=fields[2], status=fields[3], height=int(fields[4]))
	athlete.save()