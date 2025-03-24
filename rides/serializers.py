from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Ride, UserProfile

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES, write_only=True)


    def create(self, validated_data):
        role = validated_data.pop('role')  
        user = User.objects.create_user(**validated_data)
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.role = role
        user_profile.save()
        
        return user
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}


class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'

# serializer for status update        

class RideStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Ride.STATUS_CHOICES)

# serializer for location update

class RideLocationUpdateSerializer(serializers.Serializer):
    current_latitude = serializers.FloatField()
    current_longitude = serializers.FloatField()


class UserRoleSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source="profile.role")  # Fetch role from UserProfile

    class Meta:
        model = User
        fields = ['id', 'username', 'role']  # Only return necessary fields
