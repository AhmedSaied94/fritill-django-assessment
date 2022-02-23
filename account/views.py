from django.shortcuts import render

# Create your views here.


def signup(request):
    return render(request, 'account/signup.html')


def login(request):
    return render(request, 'account/login.html')


def resetPasswordRequest(request):
    return render(request, 'account/pw_reset_request.html')


def resetPasswordConfirm(request):
    return render(request, 'account/pw_reset_confirm.html')
