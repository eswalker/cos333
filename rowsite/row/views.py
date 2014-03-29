from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from row.models import Athlete, Weight, Practice, Result

# Lists athletes in a roster
def athlete_index(request):
    athletes = Athlete.objects.all()
    context = {'athletes': athletes}
    return render(request, 'row/athlete/index.html', context)

# Shows athlete details for one athlete
def athlete_detail(request, athlete_id):
    athlete = get_object_or_404(Athlete, pk=athlete_id)
    weights = Weight.objects.filter(athlete=athlete_id)
    context = {'athlete':athlete, 'weights':weights}
    return render(request, 'row/athlete/details.html', context)

# Creates a new athlete
def athlete_new(request):
    return render(request, 'row/athlete/new.html')

# Lists practices by date
def practices_index(request):
	practices = Practice.objects.all()
	context = {'practices': practices}
	return render(request, 'row/practice/index.html', context)

def athlete_detail(request, practice_id):
    athlete = get_object_or_404(Practice, pk=practice_id)
    context = {'practice':practice}
    return render(request, 'row/practice/details.html', context)



