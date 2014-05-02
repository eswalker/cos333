from django.contrib import admin
from row.models import Athlete, Practice, Piece, Result, Weight, Lineup, Boat, Note, Invite, Seat

class AthleteAdmin(admin.ModelAdmin):
	fields = ['user', 'name','year','role','side','height', 'status', 'api_key']

class ResultAdmin(admin.ModelAdmin):
	fieldsets = [
		('Date and Distance', {'fields':['datetime','distance']}),
		('More information', {'fields':['time', 'athlete','piece'], 'classes':['collapse']}),
	]


# Register your models here.
admin.site.register(Athlete, AthleteAdmin)
admin.site.register(Practice)
admin.site.register(Piece)
admin.site.register(Result, ResultAdmin)
admin.site.register(Weight)
admin.site.register(Boat)
admin.site.register(Lineup)
admin.site.register(Note)
admin.site.register(Invite)
admin.site.register(Seat)