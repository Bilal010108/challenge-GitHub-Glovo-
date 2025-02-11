from .models import *
from rest_framework import serializers



class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'age', 'profile_picture', 'gender']



class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'age', 'profile_picture', 'gender']