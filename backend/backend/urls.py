from rest_framework import permissions
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin


schema_view = get_schema_view(
   openapi.Info(
      title="Scanner API",
      default_version='v1',
      description="Our best description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="noreply@enotwebstudio.ru"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("", include("users.urls"), name="users"),
    path("", include('tests.urls'), name='tests'),
    path('admin/', admin.site.urls),
]
