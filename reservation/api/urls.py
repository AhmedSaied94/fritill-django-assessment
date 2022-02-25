from os import name
from django.urls import path

from reservation.api.views import cancel_appointment, clinic, create_appointment, create_request, get_appointments, handle_request, handle_status, requests

app_name = 'reservation_api'


urlpatterns = [
    path('clinic/<int:pk>/', clinic, name='clinic'),
    path('appointments/<str:filter>/', get_appointments, name='get-appointments'),
    path('create-appointment/',
         create_appointment, name='create-appointment'),
    path('create-request/', create_request, name='create-request'),
    path('cancel-appointment/<int:pk>/',
         cancel_appointment, name='cancel-appointment'),
    path('requests/', requests, name='requests'),
    path('handle-appointment/<int:pk>/<str:status>/',
         handle_status, name='handle-appointment'),
    path('handle-request/<int:pk>/<str:status>/',
         handle_request, name='handle-request')
]
