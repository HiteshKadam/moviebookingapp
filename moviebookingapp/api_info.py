from drf_yasg import openapi

api_info = openapi.Info(
    title="Movie Booking API",
    default_version='v1.0',
    description="API documentation for Movie Booking Application",
    contact=openapi.Contact(email="your-email@example.com"),
    license=openapi.License(name="MIT License"),
)
