from os import name
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *


app_name = 'auth'

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='get-token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('signup/', signup, name='signup'),
    path('password-reset-request/', resetPasswordRequest,
         name='password-resetrequest'),
    path('password-reset-check/<str:uid64>/<str:token>/', resetPasswordCheck,
         name='password-reset-check'),
    path('password-reset-confirm/',
         resetPasswordComplete, name='password-reset-confirm'),
]
