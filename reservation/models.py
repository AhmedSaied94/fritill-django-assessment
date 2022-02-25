from email.mime import image
from django.db import models
from django.conf import settings

# Create your models here.


class Clinic(models.Model):
    name = models.CharField(max_length=100)
    days = models.ManyToManyField('Day')
    describtion = models.TextField()
    image = models.ImageField(null=True, blank=True,
                              upload_to='clinics/images')

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    specialize = models.ForeignKey(
        'Clinic', on_delete=models.CASCADE, related_name='doctor')
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(
        'Doctor', on_delete=models.SET_NULL, null=True, related_name='appointments')
    date = models.DateTimeField()
    status = models.CharField(max_length=100, default='wating')

    def clinic(self):

        return self.doctor.specialize.name

    def __str__(self):
        return f"{self.user} have an appointment with {self.doctor} in {self.date.date()}"


class Request(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='requests')
    doctor = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField()

    def clinic(self):
        return self.doctor.specialize

    def __str__(self):
        return f"{self.user} requests an appointment with {self.doctor} in {self.date}"


class Day(models.Model):
    day = models.CharField(max_length=100)
    num = models.IntegerField(null=True)

    def __str__(self):
        return str(self.num)
