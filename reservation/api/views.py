from datetime import date, timedelta
import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from .serializers import *
from ..models import *
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.db.models import Q


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def clinic(request, pk):
    clinic_instance = Clinic.objects.get(pk=pk)
    ser_clinic = ClinicSerializer(instance=clinic_instance)
    return Response(data=ser_clinic.data, status=status.HTTP_200_OK)


@api_view(['Get'])
@permission_classes([IsAuthenticated])
def get_appointments(request, **kwargs):
    appointments = []
    if request.user.is_staff:
        appointments = Appointment.objects.all()
    else:
        appointments = Appointment.objects.filter(user=request.user)

    if kwargs['filter'] != 'all':
        filters = kwargs['filter'].split('&')

        for i in filters:
            type = i.split('=')
            if type[1] == 'all':
                continue
            if type[0] == 'date':
                appointments = appointments.filter(date__date=type[1])
            elif type[0] == 'user':
                appointments = appointments.filter(user__id=type[1])
            elif type[0] == 'status':
                if type[1] == 'upcoming':
                    appointments = appointments.filter(status='waiting')
                elif type[1] == 'past':
                    appointments = appointments.filter(
                        Q(status='finished') | Q(status='missed'))
                elif type[1] == 'finished':
                    appointments = appointments.filter(status='finished')
                elif type[1] == 'missed':
                    appointments = appointments.filter(status='missed')
    ser_apoints = AppointmentSerializer(instance=appointments, many=True)
    return Response(data=ser_apoints.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_appointment(request):
    print(request.data)
    doctor = Doctor.objects.get(pk=request.data['pk'])
    if not Appointment.objects.filter(user=request.user, doctor=doctor, status='waiting').exists():
        last_date = Appointment.objects.filter(
            status='waiting', doctor__specialize=doctor.specialize).order_by('-date').first().date
        if Appointment.objects.filter(doctor=doctor, date=last_date).count() <= 4:
            last_day = last_date.weekday()
            forward_days = ''
            clinic_days = ClinicSerializer(
                instance=Clinic.objects.get(id=doctor.specialize.id)).data['days']
            for i in range(1, 8):
                last_day += 1
                if last_day > 7:
                    last_day = 1
                if str(last_day) in clinic_days:
                    forward_days = i
                    break
            date = last_date + timedelta(days=forward_days)
            new_appointment = Appointment(
                user=request.user,
                doctor=doctor,
                date=date,
                status='waiting'
            )
            new_appointment.save()

        return Response(
            data={'success': new_appointment.__str__()},
            status=status.HTTP_201_CREATED
        )
    return Response(
        data={'failed': f'You already have an appointment with {doctor} in waiting'},
        status=status.HTTP_403_FORBIDDEN
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_request(request):
    l = request.data['date'][:10].split('-')
    if datetime.datetime.now() < datetime.datetime(int(l[0]), int(l[1]), int(l[2])):

        if not Request.objects.filter(user=request.user, doctor__id=request.data['doctor']).exists():
            ser_request = RequestSerializer(
                data={**request.data, "user": request.user.id})
            if ser_request.is_valid():
                ser_request.save()
                return Response(data={'success': f'Your request has been submitted and is waiting for approve'}, status=status.HTTP_201_CREATED)
            return Response(data=ser_request.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'error': 'You had been already requested an appointment please wait for the approve'}, status=status.HTTP_403_FORBIDDEN)
    return Response(data={'error': 'Invalid date please pick a valid one'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def requests(request):
    if request.user.is_staff:
        requests = Request.objects.all()
    else:
        requests = Request.objects.filter(user=request.user)
    try:
        ser_requests = RequestSerializer(
            instance=requests, many=True)
        return Response(data=ser_requests.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def handle_request(request, **kwargs):
    request1 = Request.objects.get(pk=kwargs['pk'])
    if kwargs['status'] == 'approve':
        new_appointment = Appointment(
            user=request1.user,
            doctor=request1.doctor,
            date=request1.date,
            status='waiting'
        )
        new_appointment.save()
        request1.delete()
        return Response(
            data={
                'success': f'you have accepted {new_appointment.user} request to meet doctor {new_appointment.doctor} in {new_appointment.date.date()}'
            },
            status=status.HTTP_201_CREATED
        )
    request1.delete()
    return Response(data={'deleted': 'you have deleted the request'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cancel_appointment(request, pk):
    appointment = Appointment.objects.get(pk=pk)
    if appointment.user == request.user or request.user.is_staff:
        appointment.delete()
        return Response(data={'deleted': 'appointment deleted successfully'}, status=status.HTTP_200_OK)

    return Response(data={'error': 'you cant delete this appointment'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['Patch'])
@permission_classes([IsAdminUser])
def handle_status(request, **kwargs):
    appointment = Appointment.objects.get(pk=kwargs['pk'])
    ser_appoint = AppointmentSerializer(
        data={"status": kwargs['status']},
        instance=appointment,
        partial=True
    )
    if ser_appoint.is_valid():
        ser_appoint.save()
        return Response(data={'success': f"status changed to {kwargs['status']}"}, status=status.HTTP_200_OK)
    return Response(data=ser_appoint.errors, status=status.HTTP_400_BAD_REQUEST)
