from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Ride
from .serializers import UserSerializer, RideSerializer

# User Registration API
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
        })

#Ride Management API
class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(rider=self.request.user)  # Assign ride to logged-in user

    # Update Ride Status (PATCH request)
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        ride = self.get_object()
        new_status = request.data.get('status')

        if new_status not in dict(Ride.STATUS_CHOICES):
            return Response({'error': 'Invalid status'}, status=400)

        ride.status = new_status
        ride.save()
        return Response(RideSerializer(ride).data)
