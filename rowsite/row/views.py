from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from row.models import Athlete, Weight, Practice, Result, Boat, Lineup
from row.forms import UserForm, UserLoginForm, AthleteForm, PracticeForm, WeightForm, ResultForm, BoatForm, LineupForm


def index(request):
    context = {'title': 'Virtual Boathouse'}
    return render(request, 'row/index.html', context)


# Lists athletes in a roster
def athlete_index(request):
    athletes = Athlete.objects.all()
    context = {'athletes': athletes}
    return render(request, 'row/athlete/index.html', context)

# Shows athlete details for one athlete
@login_required
def athlete_detail(request, athlete_id):
    athlete = get_object_or_404(Athlete, pk=athlete_id)
    weights = Weight.objects.filter(athlete=athlete_id)
    results = Result.objects.filter(athlete=athlete_id)
    context = {'athlete':athlete, 'weights':weights, 'results':results}
    return render(request, 'row/athlete/details.html', context)

# Adds a new athlete
@login_required
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

@login_required
def athlete_delete(request, id):
	athlete = get_object_or_404(Athlete, pk=id)
	athlete.delete()
	return HttpResponseRedirect(reverse('row:athlete_index'))

@login_required
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
@login_required
def practice_index(request):
	practices = Practice.objects.all()
	context = {'practices': practices}
	return render(request, 'row/practice/index.html', context)

# Shows practice details for one practice
@login_required
def practice_detail(request, practice_id):
    practice = get_object_or_404(Practice, pk=practice_id)
    results = Result.objects.filter(practice=practice_id)
    lineups = Lineup.objects.filter(practice=practice_id)
    context = {'practice':practice, 'lineups':lineups, 'results':results}
    return render(request, 'row/practice/details.html', context)

@login_required
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

@login_required
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

@login_required
def practice_delete(request, id):
	practice = get_object_or_404(Practice, pk=id)
	practice.delete()
	return HttpResponseRedirect(reverse('row:practice_index'))

# Adds a new weight
@login_required
def weight_add(request, athlete_id=None):
    if request.method == 'POST':
        form = WeightForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return athlete_index(request)
    else:
        if athlete_id == None:
            form = WeightForm()
        else:
            form = WeightForm(initial={'athlete': athlete_id})
    context = {'form':form, 'title':'Add Weight'}
    return render(request, 'row/add.html', context)

@login_required
def weight_edit(request, id):
	weight = get_object_or_404(Weight, pk=id)
	if request.method == 'POST':
		form = WeightForm(request.POST)
		if form.is_valid():
			weight.datetime = form.cleaned_data["datetime"]
			weight.athlete = form.cleaned_data["athlete"]
			weight.weight = form.cleaned_data["weight"]
			weight.save()
			return HttpResponseRedirect(reverse('row:athlete_index'))
	else:
		form = WeightForm(instance=weight)
	context = {'form':form, 'title':'Edit Weight'}
	return render(request, 'row/add.html', context)


@login_required
def weight_delete(request, id):
	weight = get_object_or_404(Weight, pk=id)
	weight.delete()
	return HttpResponseRedirect(reverse('row:athlete_index'))

# Adds a new result
@login_required
def result_add(request, practice_id=None, athlete_id=None):
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(reverse('row:practice_index'))
    else:
        if practice_id != None:
            form = ResultForm(initial={'practice': practice_id})
        elif athlete_id != None:
            form = ResultForm(initial={'athlete': athlete_id})
        else:
            form = ResultForm()
    context = {'form':form, 'title':'Add Result'}
    return render(request, 'row/add.html', context)

@login_required
def result_edit(request, id):
	result = get_object_or_404(Result, pk=id)
	if request.method == 'POST':
		form = ResultForm(request.POST)
		if form.is_valid():
			result.distance = form.cleaned_data["distance"]
			result.datetime = form.cleaned_data["datetime"]
			result.athlete = form.cleaned_data["athlete"]
			result.practice = form.cleaned_data["practice"]
			result.time = form.cleaned_data["time"]
			result.save()
			return HttpResponseRedirect(reverse('row:practice_index'))
	else:
		form = ResultForm(instance=result)
	context = {'form':form, 'title':'Edit Result'}
	return render(request, 'row/add.html', context)

@login_required
def result_delete(request, id):
	result = get_object_or_404(Result, pk=id)
	result.delete()
	return HttpResponseRedirect(reverse('row:practice_index'))

def user_register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            u = User(username=username)
            u.set_password(password)
            u.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('row:athlete_add'))
    else:
        form = UserForm()
    context = {'form':form, 'title':'Register'}
    return render(request, 'row/add.html', context)

def user_login(request):
	if request.method == 'POST':
		form = UserLoginForm(request.POST)
		username = request.POST["username"]
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				if request.GET and request.GET["next"]:
					return HttpResponseRedirect(request.GET["next"])
				return HttpResponseRedirect(reverse('row:athlete_index'))
	else:
		form = UserLoginForm()
	context = {'form':form, 'title':'Login'}
	return render(request, 'row/add.html', context)

from django.contrib.auth import logout

# Use the login_required() decorator to ensure only those logged in can logout
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('row:index'))

@login_required
def boat_index(request):
	boats = Boat.objects.all()
	context = {'boats': boats}
	return render(request, 'row/boat/index.html', context)

@login_required
def boat_add(request):
    if request.method == 'POST':
        form = BoatForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(reverse('row:boat_index'))
    else:
        form = BoatForm()
    context = {'form':form, 'title':'Add Boat'}
    return render(request, 'row/add.html', context)	

@login_required
def boat_delete(request, id):
	boat = get_object_or_404(Boat, pk=id)
	boat.delete()
	return HttpResponseRedirect(reverse('row:boat_index'))

@login_required
def boat_edit(request, id):
	boat = get_object_or_404(Boat, pk=id)
	if request.method == 'POST':
		form = BoatForm(request.POST)
		if form.is_valid():
			boat.name = form.cleaned_data["name"]
			boat.seats = form.cleaned_data["seats"]
			boat.coxed = form.cleaned_data["coxed"]
			boat.save()
			return HttpResponseRedirect(reverse('row:boat_index'))
	else:
		form = BoatForm(instance=boat)
	context = {'form':form, 'title':'Edit Boat'}
	return render(request, 'row/add.html', context)

@login_required
def lineup_add(request):
    if request.method == 'POST':
        form = LineupForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(reverse('row:practice_index'))
    else:
        form = LineupForm()
    context = {'form':form, 'title':'Add Lineup'}
    return render(request, 'row/add.html', context)

@login_required
def lineup_edit(request, id):
	lineup = get_object_or_404(Lineup, pk=id)
	if request.method == 'POST':
		form = LineupForm(request.POST)
		if form.is_valid():
			lineup.position = form.cleaned_data["position"]
			lineup.practice = form.cleaned_data["practice"]
			lineup.boat = form.cleaned_data["boat"]
			lineup.athletes = form.cleaned_data["athletes"]
			lineup.save()
			return HttpResponseRedirect(reverse('row:practice_index'))
	else:
		form = LineupForm(instance=lineup)
	context = {'form':form, 'title':'Edit Boat'}
	return render(request, 'row/add.html', context)

@login_required
def lineup_delete(request, id):
	lineup = get_object_or_404(Lineup, pk=id)
	lineup.delete()
	return HttpResponseRedirect(reverse('row:practice_index'))