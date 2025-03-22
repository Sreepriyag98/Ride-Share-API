from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RideViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'rides', RideViewSet, basename='ride')

urlpatterns = [
    path('', include(router.urls)),  # Include ViewSets
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
