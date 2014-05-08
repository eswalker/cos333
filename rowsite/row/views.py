from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt


from django.http import HttpResponse, HttpResponseRedirect, Http404

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import password_reset, password_reset_confirm, password_change
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse
from django.core import serializers

from row.models import Athlete, Weight, Practice, Piece, Result, Boat, Lineup, Note, Invite, Seat
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
    coaches = Athlete.objects.filter(role="Coach").exclude(name="COACH").order_by('name')
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

@login_required
def my_profile(request):
    user_athlete = Athlete.objects.get(user=request.user)
    return athlete_detail(request, user_athlete.id)

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
    lineups = Lineup.objects.filter(practice=practice_id)
    notes = Note.objects.filter(practice=practice_id, author=author).order_by('subject')
    permission = coxswain_coach(request.user)
    context = {'practice':practice, 'pieces':pieces, 'notes': notes, 'permission': permission, 'lineups': lineups}
    return render(request, 'row/practice/details.html', context)

"""@login_required
@user_passes_test(coxswain_coach, login_url="/denied/")
def practice_add(request):
    if request.method == 'POST':
        form = PracticeForm(request.POST)
        if form.is_valid():
            practice = form.save(commit=True)
            if practice.workout == "Erg":
                return HttpResponseRedirect(reverse('row:practice_ergroom', args=(practice.id,)))
            return HttpResponseRedirect(reverse('row:practice_detail', args=(practice.id,)))
    else:
        now = datetime.now();
        form = PracticeForm()
        form.fields['name'].initial=now.strftime("%b %d %p")
    context = {'form':form, 'title':'Add Practice'}
    return render(request, 'row/add.html', context)"""

@login_required
@user_passes_test(coxswain_coach, login_url="/denied/")
def practice_erg_add(request):

    name=datetime.now().strftime("%b %d %p")
    practice = Practice(datetime=datetime.now(), name=name, workout="Erg")
    practice.save()

    return HttpResponseRedirect(reverse('row:practice_ergroom', args=(practice.id,)))

@login_required
@user_passes_test(coach, login_url="/denied/")
def practice_water_add(request):

    name=datetime.now().strftime("%b %d %p")
    practice = Practice(datetime=datetime.now(), name=name, workout="Water")
    practice.save()

    return HttpResponseRedirect(reverse('row:practice_lineups', args=(practice.id,)))

@login_required
@user_passes_test(coxswain_coach, login_url="/denied/")
def practice_edit(request, id):
    practice = get_object_or_404(Practice, pk=id)

    if practice.workout == 'Water':
        if not coach(request.user):
            return render(request, 'row/denied.html', {})


    if request.method == 'POST':
        form = PracticeForm(request.POST)
        if form.is_valid():
            practice.name = form.cleaned_data["name"]
            practice.datetime = form.cleaned_data["datetime"]
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

    if practice.workout == 'Water':
        if not coach(request.user):
            return render(request, 'row/denied.html', {})

    practice.delete()
    return HttpResponseRedirect(reverse('row:practice_index'))

# Shows practice details for one practice
@login_required
def piece_detail(request, piece_id):
    author = Athlete.objects.get(user=request.user)
    piece = get_object_or_404(Piece, pk=piece_id)
    lineups = Lineup.objects.filter(piece=piece_id)
    
    if piece.practice.workout == "Erg":
        results = Result.objects.filter(piece=piece_id).order_by('-distance', 'time')
    else:
        results = {}
        for lineup in lineups:
            if lineup.athletes.all():
                seat = Seat.objects.filter(lineup=lineup).order_by('number')[0];
                athlete = seat.athlete
                try:
                    identifier = lineup.position + " (" + athlete.name + ")"
                    results[identifier] = Result.objects.get(piece=piece_id, athlete=athlete)
                except Result.DoesNotExist: pass

    notes = Note.objects.filter(piece=piece_id, author=author).order_by('subject')
    permission = coxswain_coach(request.user)
    is_coach = coach(request.user)
    context = {'piece':piece, 'lineups':lineups, 'results':results, 'notes': notes, 'permission': permission, 'is_coach': is_coach}
    return render(request, 'row/piece/details.html', context)

"""@login_required
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
    return render(request, 'row/add.html', context)"""

@login_required
@user_passes_test(coxswain_coach, login_url="/denied/")
def piece_edit(request, id):
    piece = get_object_or_404(Piece, pk=id)

    if piece.practice.workout == 'Water':
        if not coach(request.user):
            return render(request, 'row/denied.html', {})

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
        form.fields['practice'].queryset=Practice.objects.filter(workout=piece.practice.workout)
    context = {'form':form, 'title':'Edit Piece'}
    return render(request, 'row/add.html', context)

@login_required
@user_passes_test(coxswain_coach, login_url='/denied/')
def piece_delete(request, id):
    piece = get_object_or_404(Piece, pk=id)

    if piece.practice.workout == 'Water':
        if not coach(request.user):
            return render(request, 'row/denied.html', {})

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
            if request.GET and request.GET["next"]:
                return HttpResponseRedirect(request.GET["next"])
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

            athlete = athlete_form.save(commit=False) #TODO: strip trailing white space
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
            form.fields['username'].initial = username
            context = {'form':form, 'title':'Invalid account information'}

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

"""@login_required
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
            lineup.piece = form.cleaned_data["piece"]
            lineup.boat = form.cleaned_data["boat"]
            lineup.athletes = form.cleaned_data["athletes"]
            lineup.save()
            if request.GET and request.GET["next"]:
                return HttpResponseRedirect(request.GET["next"])
            return HttpResponseRedirect(reverse('row:practice_index'))
    else:
        form = LineupForm(instance=lineup)
    context = {'form':form, 'title':'Edit Boat'}
    return render(request, 'row/add.html', context)"""

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
        for i in range(0, len(results)/3):
            athlete_str = results[i * 3]
            time_str = results[i * 3 + 1]
            distance_str = results[i * 3 + 2]
            try:
                athlete_id = int(athlete_str)
                time = int(float(time_str) * 1000)
                distance = int(distance_str)
                if (distance > 0 and time > 0):
                    athlete = get_object_or_404(Athlete, pk=athlete_id)
                    result = Result(athlete=athlete, piece=piece, time=time, distance=distance, datetime=datetime.now())
                    result.save()
            except ValueError:
                raise Http404
        return practice_detail(request, practice_id)
    else:    
        athletes = Athlete.objects.filter(role="Rower")
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
        for i in range(0, len(results)/3):
            athlete_str = results[i * 3]
            time_str = results[i * 3 + 1]
            distance_str = results[i * 3 + 2]
            try:
                athlete_id = int(athlete_str)
                time = int(float(time_str) * 1000)
                distance = int(distance_str)
                if (distance > 0 and time > 0):
                    athlete = get_object_or_404(Athlete, pk=athlete_id)
                    result = Result(athlete=athlete, piece=piece, time=time, distance=distance, datetime=datetime.now())
                    result.save()
            except ValueError:
                raise Http404
        return practice_detail(request, practice_id)
    else:
        athletes = Athlete.objects.filter(role="Rower")
        context = {'title': 'Virtual Boathouse', 'athletes':athletes, 'practice':practice}
        return render(request, 'row/ergs-timed.html', context)

@csrf_exempt
def practice_lineups(request, practice_id):
    practice = get_object_or_404(Practice, pk=practice_id)
    if request.method == 'POST':

        # get old lineups
        old_lineups_array = []
        old_lineups = Lineup.objects.filter(practice=practice)
        for old_lineup in old_lineups:
            old_lineups_array.append(old_lineup)

        results = request.POST['results'].split(';')
        for i in range(0, len(results) - 1):
            data = results[i].split(',')
            boat_id = int(data[0])
            boat_position = data[1]
            boat_tuple = (boat_position, boat_position)
            if not boat_tuple in Lineup.position_choices:
                raise Http404
            try: 
                boat = Boat.objects.get(pk=boat_id)
                athletes = []
                lineup = Lineup(practice=practice, boat=boat, position=boat_position)
                lineup.save()
                for j in range(2, len(data) - 1):
                    athlete = Athlete.objects.get(id=int(data[j]))
                    seat = Seat(athlete=athlete, lineup=lineup, number=(j-1))
                    seat.save()
                lineup.save()
            except Boat.DoesNotExist:
                raise Http404

        # delete old lineups
        if old_lineups_array:
            for old_lineup in old_lineups_array:
                old_lineup.delete()

        return practice_detail(request, practice_id)
    else:
        boats = Boat.objects.all()
        athletes = Athlete.objects.all()
        athletes = Athlete.objects.filter(role="Rower",status="Active") | Athlete.objects.filter(role="Coxswain",status="Active")
        context = {'title': 'Virtual Boathouse', 'athletes':athletes, 'practice':practice, 'boats':boats}
        return render(request, 'row/lineups.html', context)




def denied(request):
    context = {'title': 'Permission Denied'}
    return render(request, 'row/denied.html', context)

'''

JSON API

'''

import json

def json_error(error):
    return '{ "error":"' + error + '"}'
err_coach_cox_permissions = "Only coaches and coxswains can access this resource"
err_api_key_required = "Api key required to access this resource"
err_invalid_api_key = "Api key does not match any user"
err_invalid_piece = "Invalid piece"
err_piece_required = "Piece json required to add a piece"


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
    data = serializers.serialize('json', athletes, fields=('user','name','side','role','year','status','height'))
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
def json_recent_lineups(request):
    data = json_permissions_coaches_and_coxswains(request)
    if not data:
        try:
            data = []
            practice =  Practice.objects.filter(workout='Water').latest('datetime')
            lineups = Lineup.objects.filter(practice=practice)
            data = serializers.serialize('json', lineups)
        except (Practice.DoesNotExist, Piece.DoesNotExist, Lineup.DoesNotExist):
            data = json_error("Does not exist")
    return HttpResponse(data, mimetype='application/json')

@csrf_exempt
def json_lineup_athletes(request):
    data = json_permissions_coaches_and_coxswains(request)

    if not 'id' in request.POST:
        return HttpResponse(json_error("Missing lineup id json"), mimetype='application/json')

    try: id_json = json.loads(request.POST['id'])
    except ValueError: return HttpResponse(json_error("Invalid json"), mimetype='application/json')

    if isinstance(id_json, int):
        return HttpResponse(json_error("Invalid json"), mimetype='application/json')

    if not 'id' in id_json:
        return HttpResponse(json_error("Missing lineup id in json"), mimetype='application/json')

    lineup_id = id_json['id']

    if not isinstance(lineup_id, int):
        return HttpResponse(json_error("Lineup id must be of type int"), mimetype='application/json')

    try: lineup = Lineup.objects.get(id=lineup_id)
    except Lineup.DoesNotExist:
        return HttpResponse(json_error(str(lineup_id) + " is not a valid lineup id"), mimetype='application/json')

    try:
        athletes = []
        seats = Seat.objects.filter(lineup=lineup).order_by('number')
        for seat in seats.all():
            athletes.append(seat.athlete.id)
        data = json.dumps({"athletes": athletes})
    except Seat.DoesNotExist:
        data = json_error("Lineup is empty")

    return HttpResponse(data, mimetype='application/json')





"""
@csrf_exempt
def json_practice_lineups(request, id):
    data = json_permissions_coaches_and_coxswains(request)
    if not data:
        try:
            practice = Practice.objects.get(pk=id)
            pieces = Piece.objects.filter(practice=practice)
            try:
                lineups = []
                for piece in pieces:
                    lineups.append(Lineup.objects.filter(piece=piece))
                data = serializers.serialize('json', lineups)
            except Lineup.DoesNotExist:
                data = json_error("No lineups for the practice")
        except Practice.DoesNotExist:
            data = json_error("Practice does not exist")
        except Piece.DoesNotExist:
            data = json_error("Practice does not have lineups")
    return HttpResponse(data, mimetype='application/json')"""

@csrf_exempt
def json_boats(request):
    data = json_permissions_coaches_and_coxswains(request)
    if not data:
        data = serializers.serialize('json', Boat.objects.all())
    return HttpResponse(data, mimetype='application/json')

@csrf_exempt
def json_pieces_add(request):
    data = json_permissions_coaches_and_coxswains(request)
    if data: return HttpResponse(data, mimetype='application/json')

    if not 'piece' in request.POST:
        return HttpResponse(json_error(err_piece_required), mimetype='application/json')

    try: piece_json = json.loads(request.POST['piece'])
    except ValueError: return HttpResponse(json_error("Invalid json"), mimetype='application/json')

    if not 'practice' in piece_json:
        return HttpResponse(json_error("No practice id found"), mimetype='application/json')

    practice_id = piece_json['practice']

    if not isinstance(practice_id, int):
        return HttpResponse(json_error("Practice id must be an int"), mimetype='application/json')

    try: practice = Practice.objects.get(id=practice_id)
    except Practice.DoesNotExist: return HttpResponse(json_error("Invalid practice id"), mimetype='application/json')

    if not 'name' in piece_json:
        return HttpResponse(json_error("No piece name found"), mimetype='application/json')
    name = piece_json["name"]

    if not 'datetime' in piece_json:
        return HttpResponse(json_error("No datetime found"), mimetype='application/json')
    try: piece_datetime = datetime.fromtimestamp(piece_json["datetime"])
    except Exception, e: return HttpResponse(json_error("Invalid datetime"), mimetype='application/json')

    piece = Piece(name=name, practice=practice, datetime=piece_datetime)
    piece.save()
    data = '{"id":' + str(piece.id) + '}'

    return HttpResponse(data, mimetype='application/json')

@csrf_exempt
def json_lineups_add(request):
    data = json_permissions_coaches_and_coxswains(request)
    if data: return HttpResponse(data, mimetype='application/json')

    if not 'lineup' in request.POST:
        return HttpResponse(json_error("Lineup json required to add a lineup"), mimetype='application/json')

    try: lineup_json = json.loads(request.POST['lineup'])
    except ValueError: return HttpResponse(json_error("Invalid json"), mimetype='application/json')

    if not 'athletes' in lineup_json:
        return HttpResponse(json_error("No athletes found"), mimetype='application/json')

    if not 'position' in lineup_json:
        return HttpResponse(json_error("No position found"), mimetype='application/json')

    position = lineup_json['position']
    if not ('\'' + str(position) + '\'') in str(Lineup.position_choices):
        return HttpResponse(json_error(str(position) + " is not a valid position"), mimetype='application/json')

    if not 'boat' in lineup_json:
        return HttpResponse(json_error("No boat found"), mimetype='application/json')

    boat_id = lineup_json['boat']
   
    if not isinstance(boat_id, int):
        return HttpResponse(json_error("Boat id must be of type int"), mimetype='application/json')

    try: boat = Boat.objects.get(id=boat_id)
    except Boat.DoesNotExist:
        return HttpResponse(json_error(str(boat_id) + " is not a valid boat id"), mimetype='application/json')

    if not 'piece' in lineup_json:
        return HttpResponse(json_error("No piece found"), mimetype='application/json')

    piece_id = lineup_json['piece']

    if not isinstance(piece_id, int):
        return HttpResponse(json_error("Piece id must be of type int"), mimetype='application/json')

    try: piece = Piece.objects.get(id=piece_id)
    except Piece.DoesNotExist:
        return HttpResponse(json_error(str(piece_id) + " is not a valid piece id"), mimetype='application/json')


    lineup = Lineup(position=position, boat=boat, piece=piece)
    lineup.save()

    num_coxswains, count = 0, 0;
    athletes = []
    for athlete_id in lineup_json['athletes']:
        if not isinstance(athlete_id, int):
            return HttpResponse(json_error("Athlete ids must be of type int"), mimetype='application/json')

        try:
            athlete = Athlete.objects.get(id=athlete_id)
            seat = Seat(athlete=athlete, lineup=lineup, number=count)
            seat.save()
            if athlete.role == "Coxswain": num_coxswains = num_coxswains + 1
            elif athlete.role == "Coach":
                lineup.delete()
                return HttpResponse(json_error("Athlete " + str(athlete_id) + " is a coach"), mimetype='application/json')
        except Athlete.DoesNotExist:
            lineup.delete()
            return HttpResponse(json_error(str(athlete_id) + " is not a valid athlete id"), mimetype='application/json')

        count += 1

    seats = boat.seats
    coxed = boat.coxed
    num_athletes = count

    if num_athletes != seats + coxed:
        lineup.delete()
        return HttpResponse(json_error("Boat size and number of athletes do not match"), mimetype='application/json')

    if coxed:
        if num_coxswains == 0:
            lineup.delete()
            return HttpResponse(json_error("Boat requires a coxswain"), mimetype='application/json')
        if num_coxswains > 1:
            lineup.delete()
            return HttpResponse(json_error("Lineup cannot have more than one coxswain"), mimetype='application/json')

    data = '{"id":' + str(lineup.id) + '}'

    return HttpResponse(data, mimetype='application/json')

@csrf_exempt
def json_results_add(request):
    data = json_permissions_coaches_and_coxswains(request)
    if data: return HttpResponse(data, mimetype='application/json')

    if not 'result' in request.POST:
        return HttpResponse(json_error("Result json required to add a result"), mimetype='application/json')

    try: result_json = json.loads(request.POST['result'])
    except ValueError: return HttpResponse(json_error("Invalid json"), mimetype='application/json')

    if not 'athletes' in result_json:
        return HttpResponse(json_error("No athletes found"), mimetype='application/json')

    athletes = []
    for athlete_id in result_json['athletes']:
        if not isinstance(athlete_id, int):
            return HttpResponse(json_error("Athlete ids must be of type int"), mimetype='application/json')

        try: athletes.append(Athlete.objects.get(id=athlete_id))
        except Athlete.DoesNotExist:
            return HttpResponse(json_error(str(athlete_id) + " is not a valid athlete id"), mimetype='application/json')

    if not 'piece' in result_json:
        return HttpResponse(json_error("No piece found"), mimetype='application/json')

    piece_id = result_json['piece']

    if not isinstance(piece_id, int):
        return HttpResponse(json_error("Piece id must be of type int"), mimetype='application/json')

    try: piece = Piece.objects.get(id=piece_id)
    except Piece.DoesNotExist:
        return HttpResponse(json_error(str(piece_id) + " is not a valid piece id"), mimetype='application/json')

    if not 'datetime' in result_json:
        return HttpResponse(json_error("No datetime found"), mimetype='application/json')
    try: result_datetime = datetime.fromtimestamp(result_json["datetime"])
    except Exception, e: return HttpResponse(json_error("Invalid datetime"), mimetype='application/json')

    if not 'distance' in result_json:
        return HttpResponse(json_error("No distance found"), mimetype='application/json')
    distance = result_json['distance']
    if not isinstance(distance, int):
        return HttpResponse(json_error("Distance must be of type int"), mimetype='application/json')

    if not 'time' in result_json:
        return HttpResponse(json_error("No time found"), mimetype='application/json')
    time = result_json['time']
    if not isinstance(time, int):
        return HttpResponse(json_error("Time must be of type int"), mimetype='application/json')

    for athlete in athletes:
        result = Result(athlete=athlete, distance=distance, time=time, piece=piece, datetime=result_datetime)
        result.save()

    data = '{"success": True}'
    return HttpResponse(data, mimetype='application/json')

@csrf_exempt
def json_notes_add(request):
    data = json_permissions_coaches_and_coxswains(request)
    if data: return HttpResponse(data, mimetype='application/json')

    author = Athlete.objects.get(api_key=request.POST['api_key'])

    if not 'note' in request.POST:
        return HttpResponse(json_error("Note json required to add a note"), mimetype='application/json')

    try: note_json = json.loads(request.POST['note'])
    except ValueError: return HttpResponse(json_error("Invalid json"), mimetype='application/json')

    if not 'id' in note_json:
        return HttpResponse(json_error("No id found"), mimetype='application/json')
    target_id = note_json['id']
    if not isinstance(target_id, int):
        return HttpResponse(json_error("Id must be of type int"), mimetype='application/json')

    if not 'subject' in note_json:
        return HttpResponse(json_error("No subject found"), mimetype='application/json')
    subject = note_json['subject']

    if not 'text' in note_json:
        return HttpResponse(json_error("No text found"), mimetype='application/json')
    text = note_json['text']

    note = Note(author=author, subject=subject, note=text)

    if not 'type' in note_json:
        return HttpResponse(json_error("No type found"), mimetype='application/json')  
    note_type = note_json['type']

    if note_type == 'practice':
        try: practice = Practice.objects.get(id=target_id)
        except Practice.DoesNotExist:
            return HttpResponse(json_error(str(target_id) + " is not a valid practice id"), mimetype='application/json')
        note = Note(author=author, subject=subject, note=text, practice=practice)
    
    elif note_type == 'piece':
        try: piece = Piece.objects.get(id=target_id)
        except Piece.DoesNotExist:
            return HttpResponse(json_error(str(target_id) + " is not a valid piece id"), mimetype='application/json')
        note = Note(author=author, subject=subject, note=text, piece=piece)

    else: return HttpResponse(json_error("Invalid type"), mimetype='application/json') 

    note.save()

    data = '{"id":' + str(note.id) + '}'
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
