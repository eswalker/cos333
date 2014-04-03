from django.contrib import admin
from row.models import Athlete, Practice, Result, Weight, Lineup, Boat

class AthleteAdmin(admin.ModelAdmin):
	fields = ['name','year','side','height', 'status']

class ResultAdmin(admin.ModelAdmin):
	fieldsets = [
		('Date and Distance', {'fields':['datetime','distance']}),
		('More information', {'fields':['time', 'athlete','practice'], 'classes':['collapse']}),
	]


# Register your models here.
admin.site.register(Athlete, AthleteAdmin)
admin.site.register(Practice)
admin.site.register(Result, ResultAdmin)
admin.site.register(Weight)
admin.site.register(Boat)
admin.site.register(Lineup)