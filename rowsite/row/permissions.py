#permissions.py

from django.contrib.auth.models import User

from row.models import Athlete, Weight, Practice, Piece, Result, Boat, Lineup, Note

def user_coxswain_coach(athlete1, athlete2):
	if user(athlete1, athlete2): return True
	role = athlete1.role
	if role == "Coxswain" or role == "Coach": return True
	return False

def coxswain_coach(user):
	role = Athlete.objects.get(user=user).role
	if role == "Coxswain" or role == "Coach": return True
	return False

def coach(user):
	if Athlete.objects.get(user=user).role == "Coach": return True
	return False

def user(athlete1, athlete2):
	if athlete1.pk == athlete2.pk: return True
	return False