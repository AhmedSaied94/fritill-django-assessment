from os import name
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *


app_name = 'auth'

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='get-token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('signup/', signup, name='signup')
]
