from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse


from row.models import Athlete

# Lists athletes in a roster
def athlete_index(request):
    athletes = Athlete.objects.all()
    context = {'athletes': athletes}
    return render(request, 'row/index.html', context)

# Shows athlete details for one athlete
def athlete_detail(request, athleteId):
    athlete = get_object_or_404(Athlete, pk=athleteId)
    return render(request, 'row/athlete/details.html', {'athlete':athlete})

# Creates a new athlete
def athlete_new(request):
    return render(request, 'row/athlete/new.html')

