from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers  
from drf_yasg.utils import swagger_auto_schema
from .models import Ride
from .serializers import RideStatusUpdateSerializer, UserSerializer, RideSerializer


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
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

# 🚖 Ride Management API
class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Automatically assign the logged-in user as the rider."""
        serializer.save(rider=self.request.user)

    # ✅ Correct API Documentation for Status Update
    @swagger_auto_schema(
        method='patch',
        request_body=RideStatusUpdateSerializer,  # ✅ Use the new serializer
        responses={200: RideSerializer}  # Response format
    )
    @action(detail=True, methods=['patch'], url_path='update-status')
    def update_status(self, request, pk=None):
        ride = self.get_object()
        serializer = RideStatusUpdateSerializer(data=request.data)

        if serializer.is_valid():
            ride.status = serializer.validated_data['status']
            ride.save()
            return Response({'message': 'Ride status updated', 'status': ride.status}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)