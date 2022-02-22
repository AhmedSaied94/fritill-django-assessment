from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
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
