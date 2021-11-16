from django.contrib import admin
from .models import CustomUser,Chauffeur,Demande,Passager,Taxi
# Register your models here.


admin.site.register(CustomUser)
admin.site.register(Passager)
admin.site.register(Chauffeur)
admin.site.register(Demande)
admin.site.register(Taxi)