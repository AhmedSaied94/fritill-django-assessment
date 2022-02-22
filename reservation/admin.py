from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Clinic)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Request)
admin.site.register(Day)
