from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError
from ..utils import Util
from django.urls import reverse
from django.shortcuts import redirect
from .serializers import *


@api_view(['POST'])
def signup(request):
    print(request.data)

    user = UserSerializer(data=request.data)

    if user.is_valid():
        user.save()
        return Response(data={'success': 'user created'}, status=status.HTTP_201_CREATED)
    else:
        return Response(data=user.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def resetPasswordRequest(request):
    email = request.data['email']
    if UserProfile.objects.filter(email=email).exists():
        print('good')
        user = UserProfile.objects.get(email=email)
        uid64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        redirect_url = 'http://localhost:8000/account/password-reset-confirm/'
        current_site = 'localhost:8000'
        relative_site = f"/auth/password-reset-check/{uid64}/{token}/"

        absurl = f"http://{current_site}{relative_site}"
        email_body = f"you requested an email to reset your password \n please use the link below \n {absurl}?redirect_url={redirect_url}"
        data = {
            'email_body': email_body,
            'email_subject': 'reset password request',
            'to_email': [user.email]
        }
        Util.send_email(data)
        return Response({'success': 'we sent an email with a one time link to reset your password please check your mail.'}, status=status.HTTP_200_OK)
    return Response({'error': f"{email} isn't in our database please check your email again"})


@api_view(['GET'])
def resetPasswordCheck(request, uid64, token):
    redirect_url = request.GET.get('redirect_url')
    try:
        id = smart_str(urlsafe_base64_decode(uid64))
        user = UserProfile.objects.get(id=id)
        print(user)

        if not PasswordResetTokenGenerator().check_token(user, token):
            return redirect(f"{redirect_url}?token_valid=false")

        return redirect(f"{redirect_url}?token_valid=true&uid64={uid64}&token={token}")

    except DjangoUnicodeDecodeError as error:
        return redirect(f"{redirect_url}?token_valid=false")


@api_view(['PATCH'])
def resetPasswordComplete(request):
    print(request.data)
    serializer = resetPasswordCompleteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(data={'success': 'Password reseted successfully'}, status=status.HTTP_200_OK)
    print(serializer.errors)
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
