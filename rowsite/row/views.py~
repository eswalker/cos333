from django.shortcuts import render
from django.http import HttpResponse

from row.models import Athlete

# Create your views here.
def index(request):
    athletes = Athlete.objects.all()
    output = ", ".join([a.name for a in athletes])
    return HttpResponse(output)
