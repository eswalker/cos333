from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt


from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse
from django.core import serializers

from row.models import Athlete, Weight, Practice, Piece, Result, Boat, Lineup
from row.forms import UserForm, UserLoginForm, AthleteForm, PracticeForm, PieceForm, WeightForm, ResultForm, BoatForm, LineupForm

import uuid
import csv


def index(request):
    context = {'title': 'Virtual Boathouse'}
    return render(request, 'row/index.html', context)


# Lists athletes in a roster
def athlete_index(request):
    athletes = Athlete.objects.all().order_by('name')
    context = {'athletes': athletes}
    return render(request, 'row/athlete/index.html', context)

# Shows athlete details for one athlete
@login_required
def athlete_detail(request, athlete_id):
    athlete = get_object_or_404(Athlete, pk=athlete_id)
    weights = Weight.objects.filter(athlete=athlete_id).order_by('datetime')
    results = Result.objects.filter(athlete=athlete_id).order_by('datetime')
    context = {'athlete':athlete, 'weights':weights, 'results':results}
    return render(request, 'row/athlete/details.html', context)

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
    practices = Practice.objects.all().order_by("datetime")
    context = {'practices': practices}
    return render(request, 'row/practice/index.html', context)

# Shows practice details for one practice
@login_required
def practice_detail(request, practice_id):
    practice = get_object_or_404(Practice, pk=practice_id)
    pieces = Piece.objects.filter(practice=practice_id).order_by('datetime')
    context = {'practice':practice, 'pieces':pieces}
    return render(request, 'row/practice/details.html', context)

@login_required
def practice_add(request):
    if request.method == 'POST':
        form = PracticeForm(request.POST)
        if form.is_valid():
            practice = form.save(commit=True)
            return HttpResponseRedirect(reverse('row:practice_detail', args=(practice.id,)))
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

# Shows practice details for one practice
@login_required
def piece_detail(request, piece_id):
    piece = get_object_or_404(Piece, pk=piece_id)
    results = Result.objects.filter(piece=piece_id).order_by('distance', 'time')
    lineups = Lineup.objects.filter(piece=piece_id)
    context = {'piece':piece, 'lineups':lineups, 'results':results}
    return render(request, 'row/piece/details.html', context)

@login_required
def piece_add(request, practice_id=None):
    if request.method == 'POST':
        form = PieceForm(request.POST)
        if form.is_valid():
            piece = form.save(commit=True)
            return HttpResponseRedirect(reverse('row:piece_detail', args=(piece.id,)))
    else:
        if practice_id:
            form = PieceForm(initial={'practice': practice_id})
        else:
            form = PieceForm()
    context = {'form':form, 'title':'Add Piece'}
    return render(request, 'row/add.html', context)

@login_required
def piece_edit(request, id):
    practice = get_object_or_404(Piece, pk=id)
    if request.method == 'POST':
        form = PieceForm(request.POST)
        if form.is_valid():
            piece.name = form.cleaned_data["name"]
            piece.datetime = form.cleaned_data["datetime"]
            piece.practice = form.cleaned_data["practice"]
            piece.save()
            return HttpResponseRedirect(reverse('row:practice_index'))
    else:
        form = PracticeForm(instance=practice)
    context = {'form':form, 'title':'Edit Piece'}
    return render(request, 'row/add.html', context)

@login_required
def piece_delete(request, id):
    piece = get_object_or_404(Piece, pk=id)
    piece.delete()
    return HttpResponseRedirect(reverse('row:piece_index'))


# Adds a new weight
@login_required
def weight_add(request, athlete_id=None):
    if request.method == 'POST':
        form = WeightForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            if request.GET and request.GET["next"]:
                return HttpResponseRedirect(request.GET["next"])
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
            if request.GET and request.GET["next"]:
                    return HttpResponseRedirect(request.GET["next"])
            return HttpResponseRedirect(reverse('row:athlete_index'))
    else:
        form = WeightForm(instance=weight)
    context = {'form':form, 'title':'Edit Weight'}
    return render(request, 'row/add.html', context)


@login_required
def weight_delete(request, id):
    weight = get_object_or_404(Weight, pk=id)
    weight.delete()
    if request.GET and request.GET["next"]:
        return HttpResponseRedirect(request.GET["next"])
    return HttpResponseRedirect(reverse('row:athlete_index'))

# Adds a new result
@login_required
def result_add(request, piece_id=None, athlete_id=None):
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            if request.GET and request.GET["next"]:
                return HttpResponseRedirect(request.GET["next"])
            return HttpResponseRedirect(reverse('row:practice_index'))
    else:
        if piece_id != None:
            form = ResultForm(initial={'piece': piece_id})
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
    if request.GET and request.GET["next"]:
        return HttpResponseRedirect(request.GET["next"])
    return HttpResponseRedirect(reverse('row:practice_index'))

def user_register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        athlete_form = AthleteForm(request.POST)
        if user_form.is_valid() and athlete_form.is_valid():
            username = user_form.cleaned_data["username"]
            password = user_form.cleaned_data["password"]
            u = User(username=username)
            u.set_password(password)
            u.save()

            athlete = athlete_form.save(commit=False)
            athlete.user = u
            athlete.api_key = str(uuid.uuid4())
            athlete.save()

            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('row:athlete_index'))
    else:
        user_form = UserForm()
        athlete_form = AthleteForm()
    context = {'user_form':user_form, 'athlete_form':athlete_form, 'title':'Register'}
    return render(request, 'row/register.html', context)

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
    boats = Boat.objects.all().order_by('seats')
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
def lineup_add(request, piece_id=None):
    if request.method == 'POST':
        form = LineupForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            if request.GET and request.GET["next"]:
                return HttpResponseRedirect(request.GET["next"])
            return HttpResponseRedirect(reverse('row:practice_index'))
    else:
        if piece_id == None:
            form = LineupForm()
        else:
            form = LineupForm(initial={'piece': piece_id})
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
            if request.GET and request.GET["next"]:
                return HttpResponseRedirect(request.GET["next"])
            return HttpResponseRedirect(reverse('row:practice_index'))
    else:
        form = LineupForm(instance=lineup)
    context = {'form':form, 'title':'Edit Boat'}
    return render(request, 'row/add.html', context)

@login_required
def lineup_delete(request, id):
    lineup = get_object_or_404(Lineup, pk=id)
    lineup.delete()
    if request.GET and request.GET["next"]:
        return HttpResponseRedirect(request.GET["next"])
    return HttpResponseRedirect(reverse('row:practice_index'))

@login_required
def erg(request):
    context = {'title': 'Virtual Boathouse'}
    return render(request, 'row/ergs.html', context)

'''

JSON API

'''

def json_error(error):
	return '{ "error":"' + error + '"}'
err_coach_cox_permissions = "Only coaches and coxswains can access this resource"
err_api_key_required = "Api key required to access this resource"
err_invalid_api_key = "Api key does not match any user"


# for testing
def json_permissions_coaches_and_coxswains_holder(request):
	return None

@csrf_exempt
def json_permissions_coaches_and_coxswains(request):
	if request.method == 'POST':
		api_key = request.POST['api_key']
		try:
			athlete = Athlete.objects.get(api_key=api_key)
			if athlete.is_leader():
				return None
			else:
				data = json_error(err_coach_cox_permissions)
		except Athlete.DoesNotExist:
			data = json_error(err_invalid_api_key)
	else:
		data = json_error(err_api_key_required)
	return data

@csrf_exempt
def json_athletes(request):
	athletes = Athlete.objects.all()
	data = serializers.serialize('json', athletes)
	return HttpResponse(data, mimetype='application/json')

@csrf_exempt
def json_practices(request):
	data = json_permissions_coaches_and_coxswains(request)
	if not data:
		data = serializers.serialize('json', Practice.objects.all())
	return HttpResponse(data, mimetype='application/json')

@csrf_exempt
def json_practice_lineups(request, id):
	data = json_permissions_coaches_and_coxswains(request)
	if not data:
		try:
			practice = Practice.objects.get(pk=id)
			try:
				lineups = Lineup.objects.all().filter(practice=practice)
				data = serializers.serialize('json', lineups)
			except Lineup.DoesNotExist:
				data = json_error("No lineups for the practice")
		except Practice.DoesNotExist:
			data = json_error("Practice does not exist")
	return HttpResponse(data, mimetype='application/json')

@csrf_exempt
def json_boats(request):
	data = json_permissions_coaches_and_coxswains(request)
	if not data:
		data = serializers.serialize('json', Boat.objects.all())
	return HttpResponse(data, mimetype='application/json')

@csrf_exempt
def json_login(request):
	data = None
	if request.method == 'POST':
		username = request.POST["username"]
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				try:
					athlete = Athlete.objects.get(user=user)
					data = '{"api_key":"' + athlete.api_key + '"}'
				except Athlete.DoesNotExist:
					data = None
	else:
		data = json_error("Must POST username and password")
	if data == None:
		data = json_error("Invalid username and password")
	return HttpResponse(data, mimetype='application/json')


'''

CSV


'''
def athlete_index_csv(request):
    athletes = Athlete.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="athletes.csv"'

    writer = csv.writer(response)
    for athlete in athletes:
    	data = []
    	data.append(athlete.name)
    	data.append(athlete.year)
    	data.append(athlete.side)
    	data.append(athlete.height)
    	writer.writerow(data)

    return response
