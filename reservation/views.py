from django.shortcuts import render
from .models import *

# Create your views here.


def home(request):
    clinics = Clinic.objects.all()
    rev = list(reversed(clinics))
    print(clinics.reverse())
    context = {
        'clinics': rev
    }
    return render(request, 'reservation/home.html', context)
