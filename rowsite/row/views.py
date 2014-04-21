from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt


from django.http import HttpResponse, HttpResponseRedirect, Http404

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import password_reset, password_reset_confirm, password_change
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse
from django.core import serializers

from row.models import Athlete, Weight, Practice, Piece, Result, Boat, Lineup, Note, Invite
from row.forms import UserForm, UserLoginForm, AthleteForm, PracticeForm, PieceForm, WeightForm, ResultForm, BoatForm, LineupForm, NoteForm, InviteForm, UserPasswordChangeForm

from row.permissions import user_coxswain_coach, coxswain_coach, coach, user

import uuid
import csv
from hashlib import md5

from datetime import datetime    



def index(request):
    context = {'title': 'Virtual Boathouse'}
    return render(request, 'row/index.html', context)

@login_required
@user_passes_test(coach, login_url="/denied/")
def invite_index(request):
    invites = Invite.objects.all().order_by('created_at')
    context = {'title':'Invites', 'invites': invites}
    return render(request, 'row/invite/index.html', context)

@login_required
@user_passes_test(coach, login_url="/denied/")
def invite_add(request):
    if request.method == 'POST':
        form = InviteForm(request.POST)
        if form.is_valid():
            invite = form.save(commit=False)
            invite.invite_key = md5(str(uuid.uuid4())).hexdigest()
            invite.save()
            invite.send_invite()
            return HttpResponseRedirect(reverse('row:invite_index'))
    else:
        form = InviteForm()
    context = {'form':form, 'title':'Invite'}
    return render(request, 'row/add.html', context)

@login_required
@user_passes_test(coach, login_url="/denied/")
def invite_cancel(request, id):
    invite = get_object_or_404(Invite, pk=id)
    invite.canceled = True
    invite.save()
    return HttpResponseRedirect(reverse('row:invite_index'))

# Lists athletes in a roster
def athlete_index(request):
    rowers = Athlete.objects.filter(role="Rower").order_by('name')
    coxswains = Athlete.objects.filter(role="Coxswain").order_by('name')
    coaches = Athlete.objects.filter(role="Coach").order_by('name')
    permission = False
    if not request.user.is_anonymous(): permission = coxswain_coach(request.user)
    context = {'rowers': rowers, 'coxswains': coxswains, 'coaches': coaches, 'permission': permission}
    return render(request, 'row/athlete/index.html', context)

# Shows athlete details for one athlete
@login_required
def athlete_detail(request, athlete_id):
    user_athlete = Athlete.objects.get(user=request.user)
    athlete = get_object_or_404(Athlete, pk=athlete_id)
    permission = user_coxswain_coach(user_athlete, athlete)
    is_athlete = user(user_athlete, athlete)
    weights = Weight.objects.filter(athlete=athlete_id).order_by('datetime')
    results = Result.objects.filter(athlete=athlete_id).order_by('datetime')
    context = {'athlete':athlete, 'weights':weights, 'results':results, 'permission': permission, 'is_athlete': is_athlete}
    return render(request, 'row/athlete/details.html', context)

'''
@login_required
def athlete_delete(request, id):
    athlete = get_object_or_404(Athlete, pk=id)
    user_athlete = Athlete.objects.get(user=request.user)
    if not user(user_athlete, athlete):
        context = {'title':'Permission Denied'}
        return render(request, 'row/denied.html', context)
    athlete.delete()
    return HttpResponseRedirect(reverse('row:athlete_index'))
'''

@login_required
def athlete_edit(request, athlete_id=None):
    athlete = get_object_or_404(Athlete, pk=athlete_id)
    user_athlete = Athlete.objects.get(user=request.user)
    if not user(user_athlete,  athlete):
        context = {'title':'Permission Denied'}
        return render(request, 'row/denied.html', context)
    if request.method == 'POST':
        form = AthleteForm(request.POST)
        if form.is_valid():
            athlete.name = form.cleaned_data["name"]
            athlete.side = form.cleaned_data["side"]
            athlete.year = form.cleaned_data["year"]
            athlete.height = form.cleaned_data["height"]
            athlete.status = form.cleaned_data["status"]
            athlete.save()
            if request.GET and request.GET["next"]:
                return HttpResponseRedirect(request.GET["next"])
            return HttpResponseRedirect(reverse('row:athlete_index'))
    else:
        form = AthleteForm(instance=athlete)
    context = {'form':form, 'title':'Edit Athlete'}
    return render(request, 'row/add.html', context)

# Lists practices by date
@login_required
def practice_index(request):
    practices = Practice.objects.all().order_by("datetime")
    permission = coxswain_coach(request.user)
    context = {'practices': practices, 'permission': permission}
    return render(request, 'row/practice/index.html', context)

# Shows practice details for one practice
@login_required
def practice_detail(request, practice_id):
    author = Athlete.objects.get(user=request.user)

    practice = get_object_or_404(Practice, pk=practice_id)
    pieces = Piece.objects.filter(practice=practice_id).order_by('datetime')
    notes = Note.objects.filter(practice=practice_id, author=author).order_by('subject')
    permission = coxswain_coach(request.user)
    context = {'practice':practice, 'pieces':pieces, 'notes': notes, 'permission': permission}
    return render(request, 'row/practice/details.html', context)

@login_required
@user_passes_test(coxswain_coach, login_url="/denied/")
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
@user_passes_test(coxswain_coach, login_url="/denied/")
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
@user_passes_test(coxswain_coach, login_url="/denied/")
def practice_delete(request, id):
    practice = get_object_or_404(Practice, pk=id)
    practice.delete()
    return HttpResponseRedirect(reverse('row:practice_index'))

# Shows practice details for one practice
@login_required
def piece_detail(request, piece_id):
    author = Athlete.objects.get(user=request.user)
    piece = get_object_or_404(Piece, pk=piece_id)
    results = Result.objects.filter(piece=piece_id).order_by('distance', 'time')
    lineups = Lineup.objects.filter(piece=piece_id)
    notes = Note.objects.filter(piece=piece_id, author=author).order_by('subject')
    permission = coxswain_coach(request.user)
    is_coach = coach(request.user)
    context = {'piece':piece, 'lineups':lineups, 'results':results, 'notes': notes, 'permission': permission, 'is_coach': is_coach}
    return render(request, 'row/piece/details.html', context)

@login_required
@user_passes_test(coxswain_coach, login_url="/denied/")
def piece_add(request, practice_id=None):
    if request.method == 'POST':
        form = PieceForm(request.POST)
        if form.is_valid():
            piece = form.save(commit=True)
            return HttpResponseRedirect(reverse('row:piece_detail', args=(piece.id,)))
    else:
        if practice_id:
            form = PieceForm(initial={'practice': practice_id})
            form.fields['practice'].queryset=Practice.objects.filter(id=practice_id)
        else:
            form = PieceForm()
    context = {'form':form, 'title':'Add Piece'}
    return render(request, 'row/add.html', context)

@login_required
@user_passes_test(coxswain_coach, login_url="/denied/")
def piece_edit(request, id):
    piece = get_object_or_404(Piece, pk=id)
    if request.method == 'POST':
        form = PieceForm(request.POST)
        if form.is_valid():
            piece.name = form.cleaned_data["name"]
            piece.datetime = form.cleaned_data["datetime"]
            piece.practice = form.cleaned_data["practice"]
            piece.save()
            if request.GET and request.GET["next"]:
                return HttpResponseRedirect(request.GET["next"])
            return HttpResponseRedirect(reverse('row:practice_index'))
    else:
        form = PieceForm(instance=piece)
    context = {'form':form, 'title':'Edit Piece'}
    return render(request, 'row/add.html', context)

@login_required
@user_passes_test(coxswain_coach, login_url='/denied/')
def piece_delete(request, id):
    piece = get_object_or_404(Piece, pk=id)
    piece.delete()
    if request.GET and request.GET["next"]:
        return HttpResponseRedirect(request.GET["next"])
    return HttpResponseRedirect(reverse('row:practice_index'))


# Adds a new weight
@login_required
def weight_add(request, athlete_id=None):

    athlete2 = Athlete.objects.get(user=request.user)

    if request.method == 'POST':
        form = WeightForm(request.POST, user_athlete=athlete2)
        if form.is_valid():
            form.save(commit=True)
            if request.GET and request.GET["next"]:
                return HttpResponseRedirect(request.GET["next"])
    else:
        if athlete_id == None:
            form = WeightForm(user_athlete=athlete2)
        else:
            target_athlete = get_object_or_404(Athlete, id=athlete_id)
            if not user_coxswain_coach(athlete2, target_athlete):
                return render(request, 'row/denied.html', {})
            form = WeightForm(initial={'athlete': athlete_id}, user_athlete=athlete2)
            form.fields['athlete'].queryset=Athlete.objects.filter(id=athlete_id)
    context = {'form':form, 'title':'Add Weight'}
    return render(request, 'row/add.html', context)

@login_required
def weight_edit(request, id):
    weight = get_object_or_404(Weight, pk=id)
    athlete = weight.athlete
    user_athlete = Athlete.objects.get(user=request.user)
    if not user_coxswain_coach(user_athlete, athlete):
        return render(request, 'row/denied.html', {})
    if request.method == 'POST':
        form = WeightForm(request.POST, user_athlete=user_athlete)
        if form.is_valid():
            weight.datetime = form.cleaned_data["datetime"]
            weight.athlete = form.cleaned_data["athlete"]
            weight.weight = form.cleaned_data["weight"]
            weight.save()
            if request.GET and request.GET["next"]:
                    return HttpResponseRedirect(request.GET["next"])
            return HttpResponseRedirect(reverse('row:athlete_index'))
    else:
        form = WeightForm(instance=weight, user_athlete=user_athlete)
    context = {'form':form, 'title':'Edit Weight'}
    return render(request, 'row/add.html', context)


@login_required
def weight_delete(request, id):
    weight = get_object_or_404(Weight, pk=id)
    athlete = weight.athlete
    user_athlete = Athlete.objects.get(user=request.user)
    if not user_coxswain_coach(user_athlete, athlete):
        return render(request, 'row/denied.html', {})
    weight.delete()
    if request.GET and request.GET["next"]:
        return HttpResponseRedirect(request.GET["next"])
    return HttpResponseRedirect(reverse('row:athlete_index'))

# Adds a new result
@login_required
def result_add(request, piece_id=None, athlete_id=None):
    user_athlete = Athlete.objects.get(user=request.user)

    if request.method == 'POST':
        form = ResultForm(request.POST, athlete2=user_athlete)
        if form.is_valid():
            form.save(commit=True)
            if request.GET and request.GET["next"]:
                return HttpResponseRedirect(request.GET["next"])
            return HttpResponseRedirect(reverse('row:practice_index'))
    else:
        if piece_id != None:
            form = ResultForm(initial={'piece': piece_id}, athlete2=user_athlete)
            form.fields['piece'].queryset=Piece.objects.filter(id=piece_id)
            if not coxswain_coach(user_athlete):
                form.fields['athlete'].queryset=Athlete.objects.filter(id=user_athlete.id)
        elif athlete_id != None:
            form = ResultForm(initial={'athlete': athlete_id}, athlete2=user_athlete)
            form.fields['athlete'].queryset=Athlete.objects.filter(id=athlete_id)
        else:
            form = ResultForm(athlete2=user_athlete)
    context = {'form':form, 'title':'Add Result'}
    return render(request, 'row/add.html', context)

@login_required
def result_edit(request, id):
    result = get_object_or_404(Result, pk=id)
    athlete = result.athlete
    user_athlete = Athlete.objects.get(user=request.user)
    if not user_coxswain_coach(user_athlete, athlete):
        return render(request, 'row/denied.html', {})
    if request.method == 'POST':
        form = ResultForm(request.POST, athlete2=user_athlete)
        if form.is_valid():
            result.distance = form.cleaned_data["distance"]
            result.datetime = form.cleaned_data["datetime"]
            result.athlete = form.cleaned_data["athlete"]
            result.piece = form.cleaned_data["piece"]
            result.time = form.cleaned_data["time"]
            result.save()
            return HttpResponseRedirect(reverse('row:practice_index'))
    else:
        form = ResultForm(instance=result, athlete2=user_athlete)
    context = {'form':form, 'title':'Edit Result'}
    return render(request, 'row/add.html', context)

@login_required
def result_delete(request, id):
    result = get_object_or_404(Result, pk=id)
    athlete = result.athlete
    user_athlete = Athlete.objects.get(user=request.user)
    if not user_coxswain_coach(user_athlete, athlete):
        return render(request, 'row/denied.html', {})
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
            athlete.role = invite.role
            athlete.save()

            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('row:athlete_index'))
    else:
        user_form = UserForm()
        athlete_form = AthleteForm()
    context = {'user_form':user_form, 'athlete_form':athlete_form, 'title':'Register'}
    return render(request, 'row/register.html', context)


def invited(request, invite_key):
    try:
        invite = Invite.objects.get(invite_key=invite_key)
    except Invite.DoesNotExist:
        message = "Your invite key does not exist."
        context = {'message':message}
        return render(request, 'row/denied.html', context)

    email = invite.email.lower()
    if not invite.is_recent():
        message = "Your invite is expired. Ask your coach to invite you again."
    elif invite.canceled:
        message = "Your invite has been canceled."
    elif invite.used:
        message = "Your invite has been used."
    elif User.objects.filter(username=email).exists():
        message = email + " is already registered."
    else:
        if request.method == 'POST':
            user_form = UserForm(request.POST)
            athlete_form = AthleteForm(request.POST)
            if user_form.is_valid() and athlete_form.is_valid():
                password = user_form.cleaned_data["password"]
                u = User(username=email, email=email)
                u.set_password(password)
                u.save()
                athlete = athlete_form.save(commit=False)
                athlete.user = u
                athlete.api_key = md5(str(uuid.uuid4())).hexdigest()
                athlete.role = invite.role
                athlete.save()
                invite.used = True
                invite.save()
                user = authenticate(username=email, password=password)
                login(request, user)
                return HttpResponseRedirect(reverse('row:athlete_index'))
        else:
            user_form = UserForm()
            athlete_form = AthleteForm()
        context = {'user_form':user_form, 'athlete_form':athlete_form, 'title':'Register'}
        return render(request, 'row/register.html', context)
    context = {'message':message}
    return render(request, 'row/denied.html', context)

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        username = request.POST["username"].lower()
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
    return render(request, 'row/account/login.html', context)

from django.contrib.auth import logout

# Use the login_required() decorator to ensure only those logged in can logout
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('row:index'))

def user_password_reset(request):
    return password_reset(request,
        template_name='row/account/reset.html',
        email_template_name='row/account/reset_email.html',
        subject_template_name='row/account/reset_subject.txt',
        post_reset_redirect=reverse('row:index'))

# This view handles password reset confirmation links.
# From tutorial at
# http://runnable.com/UqMu5Wsrl3YsAAfX/using-django-s-built-in-views-for-password-reset-for-python
def user_reset_confirm(request, uidb64=None, token=None):
    # Wrap the built-in reset confirmation view and pass to it all the captured parameters like uidb64, token
    # and template name, url to redirect after password reset is confirmed.
    return password_reset_confirm(request, template_name='row/account/reset_confirm.html',
        uidb64=uidb64, token=token, post_reset_redirect=reverse('row:index'))

def user_password_change(request):
    return password_change(request, template_name='row/add.html',
        post_change_redirect=reverse('row:index'),
        password_change_form=UserPasswordChangeForm,
        extra_context={'title': 'Change Password'})


@login_required
def boat_index(request):
    boats = Boat.objects.all().order_by('seats')
    permission = coxswain_coach(request.user)
    context = {'boats': boats, 'permission': permission}
    return render(request, 'row/boat/index.html', context)

@login_required
@user_passes_test(coxswain_coach, login_url='/denied/')
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
@user_passes_test(coxswain_coach, login_url='/denied/')
def boat_delete(request, id):
    boat = get_object_or_404(Boat, pk=id)
    boat.delete()
    return HttpResponseRedirect(reverse('row:boat_index'))

@login_required
@user_passes_test(coxswain_coach, login_url='/denied/')
def boat_edit(request, id):
    boat = get_object_or_404(Boat, pk=id)
    if request.method == 'POST':
        form = BoatForm(request.POST)
        if form.is_valid():
            boat.name = form.cleaned_data["name"]
            boat.seats = form.cleaned_data["seats"]
            if form.cleaned_data["coxed"] == "True":
                boat.coxed = True
            else:
                boat.coxed = False
            boat.save()
            return HttpResponseRedirect(reverse('row:boat_index'))
    else:
        form = BoatForm(instance=boat)
    context = {'form':form, 'title':'Edit Boat'}
    return render(request, 'row/add.html', context)

@login_required
@user_passes_test(coach, login_url='/denied/')
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
            form.fields['piece'].queryset=Piece.objects.filter(id=piece_id)
    context = {'form':form, 'title':'Add Lineup'}
    return render(request, 'row/add.html', context)

@login_required
@user_passes_test(coach, login_url='/denied/')
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
@user_passes_test(coach, login_url='/denied/')
def lineup_delete(request, id):
    lineup = get_object_or_404(Lineup, pk=id)
    lineup.delete()
    if request.GET and request.GET["next"]:
        return HttpResponseRedirect(request.GET["next"])
    return HttpResponseRedirect(reverse('row:practice_index'))

@login_required
def note_add(request, piece_id=None, practice_id=None):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.author = Athlete.objects.get(user=request.user)
            if piece_id: note.piece = Piece.objects.get(pk=piece_id)
            elif practice_id: note.practice = Practice.objects.get(pk=practice_id)
            note.save()
            if request.GET and request.GET["next"]:
                return HttpResponseRedirect(request.GET["next"])
            return HttpResponseRedirect(reverse('row:practice_index'))
    else:
        form = NoteForm()
    context = {'form':form, 'title':'Add Note'}
    return render(request, 'row/add.html', context) 

"""
@login_required
def note_detail(request, id):
    note = get_object_or_404(Note, pk=id)
    context = {'note':note}
    return render(request, 'row/note/details.html', context)"""

@login_required
def note_edit(request, id):
    note = get_object_or_404(Note, pk=id)
    athlete = note.author
    user_athlete = Athlete.objects.get(user=request.user)
    if not user(user_athlete, athlete):
        return render(request, 'row/denied.html', {})
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note.subject = form.cleaned_data["subject"]
            note.note = form.cleaned_data["note"]
            note.save()
            if request.GET and request.GET["next"]:
                return HttpResponseRedirect(request.GET["next"])
            return HttpResponseRedirect(reverse('row:practice_index'))
    else:
        form = NoteForm(instance=note)
    context = {'form':form, 'title':'Edit Note'}
    return render(request, 'row/add.html', context)

@login_required
def note_delete(request, id):
    note = get_object_or_404(Note, pk=id)
    athlete = note.author
    user_athlete = Athlete.objects.get(user=request.user)
    if not user(user_athlete, athlete):
        return render(request, 'row/denied.html', {})
    note.delete()
    if request.GET and request.GET["next"]:
        return HttpResponseRedirect(request.GET["next"])
    return HttpResponseRedirect(reverse('row:practice_index'))

@login_required
def erg(request):
	athletes = Athlete.objects.all()
	context = {'title': 'Virtual Boathouse', 'athletes':athletes}
	return render(request, 'row/ergs.html', context)

@csrf_exempt
def practice_ergroom(request, practice_id):
	practice = get_object_or_404(Practice, pk=practice_id)
	if request.method == 'POST':
		name = request.POST['name']
		results = request.POST['results'].split(',')				
		piece = Piece(practice=practice, name=name, datetime=datetime.now())
		piece.save()
		print results
		for i in range(0, len(results)/3):
			athlete_str = results[i * 3]
			time_str = results[i * 3 + 1]
			distance_str = results[i * 3 + 2]
			try:
				athlete_id = int(athlete_str)
				time = int(float(time_str) * 10) / 10.
				distance = int(distance_str)
				if (distance > 0 and time > 0):
					athlete = get_object_or_404(Athlete, pk=athlete_id)
					result = Result(athlete=athlete, piece=piece, time=time, distance=distance, datetime=datetime.now())
					result.save()
			except ValueError:
				raise Http404
		return practice_detail(request, practice_id)
	else:	
		athletes = Athlete.objects.all()
		context = {'title': 'Virtual Boathouse', 'athletes':athletes, 'practice':practice}
		return render(request, 'row/ergs.html', context)

@csrf_exempt
def practice_ergroom_timed(request, practice_id):
	practice = get_object_or_404(Practice, pk=practice_id)
	if request.method == 'POST':
		name = request.POST['name']
		results = request.POST['results'].split(',')				
		piece = Piece(practice=practice, name=name, datetime=datetime.now())
		piece.save()
		print results
		for i in range(0, len(results)/3):
			athlete_str = results[i * 3]
			time_str = results[i * 3 + 1]
			distance_str = results[i * 3 + 2]
			try:
				athlete_id = int(athlete_str)
				time = int(float(time_str) * 10) / 10.
				distance = int(distance_str)
				if (distance > 0 and time > 0):
					athlete = get_object_or_404(Athlete, pk=athlete_id)
					result = Result(athlete=athlete, piece=piece, time=time, distance=distance, datetime=datetime.now())
					result.save()
			except ValueError:
				raise Http404
		return practice_detail(request, practice_id)
	else:	
		athletes = Athlete.objects.all()
		context = {'title': 'Virtual Boathouse', 'athletes':athletes, 'practice':practice}
		return render(request, 'row/ergs-timed.html', context)

def denied(request):
    context = {'title': 'Permission Denied'}
    return render(request, 'row/denied.html', context)

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
def json_recent_practice(request):
	data = json_permissions_coaches_and_coxswains(request)
	if not data:
		try:
			practice =  Practice.objects.filter(workout='Water').latest('datetime')
			data = '{"id":' + str(practice.id) + '}'
		except Practice.DoesNotExist:
			data = json_error("Does not exist")
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
