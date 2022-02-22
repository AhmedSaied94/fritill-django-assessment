from django.urls import path
from .views import *

app_name = 'reserve'

urlpatterns = [
    path('', home, name='home')
]
