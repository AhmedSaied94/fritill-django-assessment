from os import name
from django.urls import path
from .views import *

app_name = 'account'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('password-reset-request/', resetPasswordRequest,
         name='password-reset-request'),
    path('password-reset-confirm/', resetPasswordConfirm,
         name='password-reset-confirm')
]
