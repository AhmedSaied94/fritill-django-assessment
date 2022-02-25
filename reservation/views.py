
from django.shortcuts import render
from .models import *
from .api.serializers import *
from account.models import UserProfile

# Create your views here.


def home(request):
    clinics = Clinic.objects.all()
    rev = list(reversed(clinics))
    print(clinics.reverse())
    context = {
        'clinics': rev
    }
    return render(request, 'reservation/home.html', context)


def clinic(request, pk):
    try:
        clinic = Clinic.objects.get(pk=pk)
        rec = ClinicSerializer(instance=clinic).data
        print(rec)
        context = {'clinic': rec}
    except Exception as e:
        context = {'error': str(e)}

    return render(request, 'reservation/clinic.html', context={"pk": pk, 'clinic': clinic})


def request_appointment(request, pk):
    doctor = Doctor.objects.get(pk=pk)
    ser_doc = DoctorSerializer(instance=doctor)
    print(ser_doc.data)
    return render(request, 'reservation/request.html', context={"doctor": ser_doc.data})


def my_appointments(request):
    return render(request, 'reservation/my_appointments.html')


def admin_panel(request, pk):
    if UserProfile.objects.get(pk=pk).is_staff:
        return render(request, 'reservation/admin.html')
    return render(request, 'reservation/404.html')
