#permissions.py

from django.contrib.auth.models import User

from row.models import Athlete, Weight, Practice, Piece, Result, Boat, Lineup, Note

def user_coxswain_coach(user, athlete):
	if user(user, athlete): return True
	return coxswain_coach(user)

def coxswain_coach(user):
	side = Athlete.objects.get(user=user).side
	if side == "Coxswain" or side == "Coach": return True
	return False

def coach(user):
	if Athlete.objects.get(user=user).side == "Coach": return True
	return False

def user(user, athlete):
	if Athlete.objects.get(user=user).pk == athlete.pk: return True
	return False