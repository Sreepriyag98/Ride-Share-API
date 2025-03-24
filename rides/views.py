from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers  
from drf_yasg.utils import swagger_auto_schema
from .models import Ride, UserProfile
from .serializers import RideStatusUpdateSerializer, UserSerializer, RideSerializer,RideLocationUpdateSerializer, UserRoleSerializer


#  User Registration API
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate JWT token after registration
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': serializer.data,
        }, status=status.HTTP_201_CREATED)
    
    # for role
    @swagger_auto_schema(
    method='get',
    responses={200: UserRoleSerializer}  
)
    @action(detail=False, methods=['get'], url_path='my-role', permission_classes=[IsAuthenticated])
    def my_role(self, request):
        serializer = UserRoleSerializer(request.user) 
        return Response(serializer.data, status=status.HTTP_200_OK)

    #for all users
    @action(detail=False, methods=['get'], url_path='all-users-role', permission_classes=[IsAuthenticated])
    def all_users(self, request):
        """  Returns a list of all users with their roles. """
        users = User.objects.all()
        serializer = UserRoleSerializer(users, many=True)  # Serialize multiple users
        return Response(serializer.data, status=status.HTTP_200_OK)

#  Ride Management API
class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Automatically assign the logged-in user as the rider."""
        serializer.save(rider=self.request.user)

    #  For Status Update API

    @swagger_auto_schema(
        method='patch',
        request_body=RideStatusUpdateSerializer,  
        responses={200: RideSerializer}  
    )
    @action(detail=True, methods=['patch'], url_path='update-status')
    def update_status(self, request, pk=None):
        ride = self.get_object()
        if request.user != ride.driver and request.user != ride.rider:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        serializer = RideStatusUpdateSerializer(data=request.data)

        if serializer.is_valid():
            ride.status = serializer.validated_data['status']
            ride.save()
            return Response({'message': 'Ride status updated', 'status': ride.status}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# for real time Location API

    @swagger_auto_schema(
        method='patch',
        request_body=RideLocationUpdateSerializer,
        responses={200: RideSerializer}  
    )
    @action(detail=True, methods=['patch'], url_path='update-location')
    def update_location(self, request, pk=None):
        """
        Driver updates their current location.
        Only 'current_latitude' & 'current_longitude' are accepted.
        """
        ride = self.get_object()

        #  Ensure only the assigned driver can update location
        if ride.driver != request.user:
            return Response({'error': 'Only the driver can update location'}, status=status.HTTP_403_FORBIDDEN)

        #  Validate request payload using serializer
        serializer = RideLocationUpdateSerializer(data=request.data)
        if serializer.is_valid():
            ride.current_latitude = serializer.validated_data['current_latitude']
            ride.current_longitude = serializer.validated_data['current_longitude']
            ride.save()

            return Response({
               'message': 'Location updated successfully',
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #  Filter Rides for Drivers
    @action(detail=False, methods=['get'], url_path='my-driver-rides')
    def my_driver_rides(self, request):
        rides = Ride.objects.filter(driver=request.user)
        serializer = RideSerializer(rides, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #  Filter Rides for Riders
    @action(detail=False, methods=['get'], url_path='my-rider-rides')
    def my_rider_rides(self, request):
        rides = Ride.objects.filter(rider=request.user)
        serializer = RideSerializer(rides, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)