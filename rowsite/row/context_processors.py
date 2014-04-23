from row.models import Athlete

from django.contrib.auth.models import User


def add_role(request):
	if request.user.is_anonymous():
		return {'anonymous': 'anonymous'}
	else:
		athlete = Athlete.objects.get(user=request.user)
		return {'role': athlete.role,}