from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

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
def athlete_add(request):
    if request.method == 'POST':
        form = AthleteForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(reverse('row:athlete_index'))
    else:
        form = AthleteForm()

	context = {'form':form, 'title':'Add Athlete'}
	return render(request, 'row/add.html', context)

def athlete_delete(request, id):
	athlete = get_object_or_404(Athlete, pk=id)
	athlete.delete()
	return HttpResponseRedirect(reverse('row:athlete_index'))

def athlete_edit(request, athlete_id=None):
	athlete = get_object_or_404(Athlete, pk=athlete_id)
	if request.method == 'POST':
		form = AthleteForm(request.POST)
		if form.is_valid():
			athlete.name = form.cleaned_data["name"]
			athlete.side = form.cleaned_data["side"]
			athlete.year = form.cleaned_data["year"]
			athlete.height = form.cleaned_data["height"]
			athlete.status = form.cleaned_data["status"]
			athlete.save()
			return HttpResponseRedirect(reverse('row:athlete_index'))
	else:
		form = AthleteForm(instance=athlete)
	context = {'form':form, 'title':'Edit Athlete'}
	return render(request, 'row/add.html', context)

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

def practice_add(request):
	if request.method == 'POST':
		form = PracticeForm(request.POST)
		if form.is_valid():
			form.save(commit=True)
			return HttpResponseRedirect(reverse('row:practice_index'))
	else:
		form = PracticeForm()
	context = {'form':form, 'title':'Add Practice'}
	return render(request, 'row/add.html', context)

def practice_edit(request, id):
	practice = get_object_or_404(Practice, pk=id)
	if request.method == 'POST':
		form = PracticeForm(request.POST)
		if form.is_valid():
			practice.name = form.cleaned_data["name"]
			practice.datetime = form.cleaned_data["datetime"]
			practice.workout = form.cleaned_data["workout"]
			practice.save()
			return HttpResponseRedirect(reverse('row:practice_index'))
	else:
		form = PracticeForm(instance=practice)
	context = {'form':form, 'title':'Edit Practice'}
	return render(request, 'row/add.html', context)

def practice_delete(request, id):
	practice = get_object_or_404(Practice, pk=id)
	practice.delete()
	return HttpResponseRedirect(reverse('row:practice_index'))

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
	context = {'form':form, 'title':'Add Weight'}
	return render(request, 'row/add.html', context)

def weight_delete(request, id):
	weight = get_object_or_404(Weight, pk=id)
	weight.delete()
	return HttpResponseRedirect(reverse('row:athlete_index'))

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
	context = {'form':form, 'title':'Add Result'}
	return render(request, 'row/add.html', context)

def result_delete(request, id):
	result = get_object_or_404(Result, pk=id)
	result.delete()
	return HttpResponseRedirect(reverse('row:practice_index'))

