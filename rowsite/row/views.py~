from django.shortcuts import render
from django.http import HttpResponse

from row.models import Athlete

# Create your views here.
def index(request):
    athletes = Athlete.objects.all()
    context = {'athletes': athletes}
    return render(request, 'row/index.html', context)
