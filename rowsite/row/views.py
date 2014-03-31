from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS

from row.models import Athlete, Weight, Practice, Result
from row.forms import AthleteForm, PracticeForm, WeightForm, ResultForm

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

# Adds a new athlete
def athlete_add(request, athlete_id=None):
    if athlete_id:
        athlete = get_object_or404(Athlete, pk=athlete_id)

    else:
        athlete = Athlete()

    if request.method == 'POST':
        form = AthleteForm(request.POST, instance=athlete)
        if form.is_valid():
            form.save(commit=True)
            return athlete_index(request)
            
        else:
			print form.errors
    else:
        form = AthleteForm()

	context = {'form':form}
	return render(request, 'row/athlete/add.html', context)

# Lists practices by date
def practice_index(request):
	practices = Practice.objects.all()
	context = {'practices': practices}
	return render(request, 'row/practice/index.html', context)

# Shows practice details for one practice
def practice_detail(request, practice_id):
    practice = get_object_or_404(Practice, pk=practice_id)
    results = Result.objects.filter(practice=practice_id)
    context = {'practice':practice, 'results':results}
    return render(request, 'row/practice/details.html', context)

# Adds a new practice
def practice_add(request, id=None):
	if request.method == 'POST':
		form = PracticeForm(request.POST)
		if form.is_valid():
			form.save(commit=True)
			return practice_index(request)
		else:
			print form.errors
	else:
		practice = None
		if id:
			practice = get_object_or_404(Practice, pk=id)
		if practice:
			form = PracticeForm(instance=practice)
		else:
			form = PracticeForm()
	context = {'form':form}
	return render(request, 'row/practice/add.html', context)



# Adds a new weight
def weight_add(request, athlete_id=None):
    if request.method == 'POST':
        form = WeightForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return athlete_index(request)
        else:
            print form.errors
    else:
    	if athlete_id == None:
        	form = WeightForm()
    	else:
        	form = WeightForm(initial={'athlete': athlete_id})
    context = {'form':form}
    return render(request, 'row/weight/add.html', context)

# Adds a new result
def result_add(request, practice_id=None, athlete_id=None):
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return practice_index(request)
        else:
            print form.errors

    if practice_id != None:
        form = ResultForm(initial={'practice': practice_id})
    elif athlete_id != None:
        form = ResultForm(initial={'athlete': athlete_id})
    else:
        form = ResultForm()
    context = {'form':form}
    return render(request, 'row/result/add.html', context)
