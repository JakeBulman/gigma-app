from django.contrib import admin
from account.models import Discipline

# Register your models here.
class DisciplineAdmin(admin.ModelAdmin):
    pass


admin.site.register(Discipline)