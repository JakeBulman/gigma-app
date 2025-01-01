from django.contrib import admin
from account.models import Discipline,Profile

# Register your models here.
class DisciplineAdmin(admin.ModelAdmin):
    pass

class ProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(Discipline)
admin.site.register(Profile)