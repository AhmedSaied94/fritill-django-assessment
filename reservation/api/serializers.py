from os import name
from re import A
from ..models import *
from rest_framework import serializers, fields


class NewRepresent(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value


class ClinicSerializer(serializers.ModelSerializer):
    doctor = serializers.SerializerMethodField()
    days = NewRepresent(many=True)

    class Meta:
        model = Clinic
        fields = ['name', 'days', 'describtion', 'image', 'doctor']

    def get_doctor(self, obj):
        if obj.doctor.all():
            return DoctorSerializer(obj.doctor.all(), many=True).data


class DoctorSerializer(serializers.ModelSerializer):
    appointments = serializers.SerializerMethodField()
    specialize = NewRepresent()

    class Meta:
        model = Doctor
        fields = ['id', 'name', 'age', 'specialize', 'bio', 'appointments']

    def get_appointments(self, obj):
        if obj.appointments.all():
            return AppointmentSerializer(obj.appointments.all(), many=True).data


class AppointmentSerializer(serializers.ModelSerializer):

    user = NewRepresent()
    date = NewRepresent()
    doctor = NewRepresent()
    clinic = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = ['id', 'user', 'doctor', 'date', 'status', 'clinic']

    def get_clinic(self, obj):
        cli = Clinic.objects.get(name=obj.doctor.specialize)
        return cli.name


class RequestSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(input_formats=['%Y-%m-%dT%H:%M:%S'])
    clinic = serializers.SerializerMethodField()
    request_user = serializers.SerializerMethodField()
    request_doctor = serializers.SerializerMethodField()

    class Meta:
        model = Request
        fields = ['id', 'user', 'doctor', 'date', 'clinic',
                  'request_user', 'request_doctor']

    def get_request_user(self, obj):
        return obj.user.username

    def get_request_doctor(self, obj):
        return obj.doctor.name

    def get_clinic(self, obj):
        cli = Clinic.objects.get(name=obj.doctor.specialize)
        return cli.name
