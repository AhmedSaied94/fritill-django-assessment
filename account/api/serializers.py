from rest_framework import serializers
from ..models import *
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    # appointments = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'email',
            'username',
            'password',
            'first_name',
            'last_name',
            'age',
            'gender',
            # 'appointments',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def save(self, **kwargs):
        user = UserProfile(
            email=self.validated_data.get('email'),
            username=self.validated_data.get('username'),
            first_name=self.validated_data.get('first_name'),
            last_name=self.validated_data.get('last_name'),
            age=self.validated_data.get('age'),
            gender=self.validated_data.get('gender'),
        )

        user.set_password(self.validated_data.get('password'))
        user.save()
        return user

    # def get_appointments(self, obj):
    #     if obj.following:
    #         return FollowingSerializer(obj.following.all(), many=True).data


class resetPasswordCompleteSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    uid64 = serializers.CharField(required=True)
    token = serializers.CharField(required=True)

    class Meta:
        fields = ['password', 'uid64', 'token']

    def validate_password(self, value):
        try:
            validate_password(value)
        except Exception as e:
            raise serializers.ValidationError(str(e), code=400)
        return value

    def save(self, **kwargs):

        uid64 = self.validated_data['uid64']
        token = self.validated_data['token']
        id = smart_str(urlsafe_base64_decode(uid64))
        user = UserProfile.objects.get(id=id)
        print(user, token)

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise AuthenticationFailed(
                detail='link has been expired', code=401)

        user.set_password(self.validated_data['password'])
        user.save()
        return user
