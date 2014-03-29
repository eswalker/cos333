from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from row.models import Athlete, Weight, Practice, Result

# Lists athletes in a roster
def athlete_index(request):
    athletes = Athlete.objects.all()
    context = {'athletes': athletes}
    return render(request, 'row/athlete/index.html', context)

# Shows athlete details for one athlete
def athlete_detail(request, athleteId):
    athlete = get_object_or_404(Athlete, pk=athleteId)
    weights = Weight.objects.filter(athlete=athleteId)
    return render(request, 'row/athlete/details.html', {'athlete':athlete, 'weights':weights})

# Creates a new athlete
def athlete_new(request):
    return render(request, 'row/athlete/new.html')

# Lists practices by date
def practices_index(request):
	practices = Practice.objects.all()
	context = {'practices': practices}
	return render(request, 'row/practice/index.html', context)



