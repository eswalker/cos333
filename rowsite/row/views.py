from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse


from row.models import Athlete

# Create your views here.
def index(request):
    athletes = Athlete.objects.all()
    context = {'athletes': athletes}
    return render(request, 'row/index.html', context)

''' my comment '''
def detail(request, athleteId):
    athlete = get_object_or_404(Athlete, pk=athleteId)
    return render(request, 'row/athlete/details.html', {'athlete':athlete})

def new(request):
    return render(request, 'row/athlete/new.html')
