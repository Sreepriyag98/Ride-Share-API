from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserViewSet, RideViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'rides', RideViewSet, basename='ride')

urlpatterns = [
    path('', include(router.urls)),  # ✅ Users & Rides endpoints
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # ✅ Fix login endpoint
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
