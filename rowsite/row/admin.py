from django.contrib import admin
from row.models import Athlete, Practice, Result, Weight

# Register your models here.
admin.site.register(Athlete)
admin.site.register(Practice)
admin.site.register(Result)
admin.site.register(Weight)