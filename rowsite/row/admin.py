from django.contrib import admin
from row.models import Athlete, Practice, Result, Weight

class AthleteAdmin(admin.ModelAdmin):
	fields = ['name','year','height','side']

# Register your models here.
admin.site.register(Athlete, AthleteAdmin)
admin.site.register(Practice)
admin.site.register(Result)
admin.site.register(Weight)