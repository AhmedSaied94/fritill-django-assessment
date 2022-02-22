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
    specialize = models.ForeignKey('Clinic', on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    days = models.ManyToManyField('Day')

    def __str__(self):
        return self.name


class Appointment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    doctor = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField()
    missed = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)

    def clinic(self):
        return self.doctor.specialize

    def __str__(self):
        return f"{self.user} have an appointment with {self.doctor} in {self.date}"


class Request(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    doctor = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField()
    approved = models.BooleanField(default=False)

    def clinic(self):
        return self.doctor.specialize

    def __str__(self):
        return f"{self.user} requests an appointment with {self.doctor} in {self.date}"


class Day(models.Model):
    day = models.CharField(max_length=100)

    def __str__(self):
        return self.day
