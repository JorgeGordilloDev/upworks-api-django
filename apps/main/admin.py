from django.contrib.admin import ModelAdmin, register
from .models import *

@register(Alumn)
class AlumnAdmin(ModelAdmin):
   list_display = ('id', 'user', 'matricula',)
   list_display_links = ('user',)
   search_fields = ("user__name", "user__email")
   actions = None
   filter_horizontal = ()

@register(Company)
class CompanyAdmin(ModelAdmin):
   pass

@register(Job)
class JobAdmin(ModelAdmin):
   pass

@register(Applications)
class ApplicationAdmin(ModelAdmin):
   pass