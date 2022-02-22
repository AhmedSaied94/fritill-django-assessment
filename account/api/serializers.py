from rest_framework import serializers
from ..models import *


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
