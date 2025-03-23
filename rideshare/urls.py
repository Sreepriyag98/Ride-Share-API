"""
URL configuration for rideshare project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic import TemplateView

# 🔹 Swagger Schema Configuration
schema_view = get_schema_view(
    openapi.Info(
        title="Ride Sharing API",
        default_version='v1',
        description="API documentation for the ride-sharing application",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('rides.urls')), 
    re_path(r'^swagger/$', TemplateView.as_view(
        template_name='drf-yasg/swagger-ui.html',
        extra_context={'schema_url': 'schema-json'}
    ), name='swagger-ui'),

    # ✅ Alternative ReDoc UI
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-ui'),

    # ✅ Raw JSON Schema
    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]

