from django.contrib import admin
from .models import Registrations, APs, Customers, Towers

# Register your models here.

admin.site.register(Registrations)
admin.site.register(Customers)
admin.site.register(APs)
admin.site.register(Towers)