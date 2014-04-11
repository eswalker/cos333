#permissions.py

from django.contrib.auth.models import User

from row.models import Athlete, Weight, Practice, Piece, Result, Boat, Lineup, Note

def user_coxswain_coach(athlete1, athlete2):
	if user(athlete1, athlete2): return True

	side = athlete1.side
	if side == "Coxswain" or side == "Coach": return True
	return False

def coxswain_coach(user):
	side = Athlete.objects.get(user=user).side
	if side == "Coxswain" or side == "Coach": return True
	return False

def coach(user):
	if Athlete.objects.get(user=user).side == "Coach": return True
	return False

def user(athlete1, athlete2):
	if athlete1.pk == athlete2.pk: return True
	return False