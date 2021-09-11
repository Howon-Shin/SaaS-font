from django.contrib import admin
from .models import Proj, HUser, OwnerShip

# Register your models here.
admin.site.register(Proj)
admin.site.register(HUser)
admin.site.register(OwnerShip)