from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from row.models import Athlete, Weight, Practice, Result
from row.forms import PracticeForm

# Lists athletes in a roster
def athlete_index(request):
    athletes = Athlete.objects.all()
    context = {'athletes': athletes}
    return render(request, 'row/athlete/index.html', context)

# Shows athlete details for one athlete
def athlete_detail(request, athlete_id):
    athlete = get_object_or_404(Athlete, pk=athlete_id)
    weights = Weight.objects.filter(athlete=athlete_id)
    results = Result.objects.filter(athlete=athlete_id)
    context = {'athlete':athlete, 'weights':weights, 'results':results}
    return render(request, 'row/athlete/details.html', context)

# Creates a new athlete
def athlete_new(request):
    return render(request, 'row/athlete/new.html')

# Lists practices by date
def practice_index(request):
	practices = Practice.objects.all()
	context = {'practices': practices}
	return render(request, 'row/practice/index.html', context)

# Shows practice details for one practice
def practice_detail(request, practice_id):
    practice = get_object_or_404(Practice, pk=practice_id)
    context = {'practice':practice}
    return render(request, 'row/practice/details.html', context)

# Creates a new practice
def practice_new(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = PracticeForm(request.POST)

        if form.is_valid():
            form.save(commt=True)
            return practice_index(request)

        else:
            print form.errors

    else:
        form = PracticeForm()

    return render_toPresponse('row/practice/new.html', {'form': form}, context)




