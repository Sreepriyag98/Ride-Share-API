from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Ride

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

class RideSerializer(serializers.ModelSerializer):
    rider = serializers.ReadOnlyField(source='rider.username')
    driver = serializers.ReadOnlyField(source='driver.username')

    class Meta:
        model = Ride
        fields = '__all__'
