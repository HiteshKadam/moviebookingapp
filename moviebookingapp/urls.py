from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

api_schema_view = get_schema_view(
    openapi.Info(
        title="Movie Booking API",
        default_version='v1.0',
        description="API documentation for Movie Booking Application",
        contact=openapi.Contact(email="admin@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1.0/moviebooking/', include('movies.urls')),
    path('api/v1.0/moviebooking/', include('accounts.urls')),
    path('swagger/', api_schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('api/doc/', api_schema_view.with_ui('redoc', cache_timeout=0), name='api-doc'),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)