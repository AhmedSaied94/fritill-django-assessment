from django.urls import path
from .views import *

app_name = 'reservation'

urlpatterns = [
    path('', home, name='home'),
    path('clinic/<int:pk>/', clinic, name='clinic'),
    path('request-appointment/<int:pk>/',
         request_appointment, name='request-appointment'),
    path('my-appointments/', my_appointments, name='my-appointments'),
    path('admin-panel/<int:pk>/', admin_panel, name='admin-panel')
]
