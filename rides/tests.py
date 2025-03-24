from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Ride, UserProfile

class ModelTests(TestCase):
    def setUp(self):
        self.rider = User.objects.create_user(username="rider123", password="testpass")
        self.driver = User.objects.create_user(username="driver123", password="testpass")

        #  Manually update UserProfile roles
        self.rider.profile.role = "rider"
        self.rider.profile.save()
        self.driver.profile.role = "driver"
        self.driver.profile.save()

    def test_user_profile_creation(self):
        self.assertEqual(self.rider.profile.role, "rider")  
        self.assertEqual(self.driver.profile.role, "driver")

    def test_ride_creation(self):
        ride = Ride.objects.create(
            rider=self.rider,
            pickup_location="123 Main St",
            dropoff_location="456 Elm St"
        )
        self.assertEqual(ride.status, "REQUESTED")  
        self.assertIsNone(ride.driver)  



class APITests(APITestCase):
    def setUp(self):
        self.rider = User.objects.create_user(username="rider123", email="rider123@example.com", password="testpass")
        self.driver = User.objects.create_user(username="driver123", email="driver123@example.com", password="testpass")

        #  Django signals will create UserProfile automatically

        self.ride = Ride.objects.create(
            rider=self.rider,
            pickup_location="123 Main St",
            dropoff_location="456 Elm St"
        )

        #  Get JWT tokens
        self.rider_token = str(RefreshToken.for_user(self.rider).access_token)
        self.driver_token = str(RefreshToken.for_user(self.driver).access_token)

    def test_rider_creates_ride(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.rider_token}")
    
        data = {
            "rider": self.rider.id,  
            "pickup_location": "789 Oak St",
            "dropoff_location": "101 Pine St"
        }
    
        response = self.client.post("/api/rides/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    
