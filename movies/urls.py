from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, TicketViewSet,TicketViewSetAdmin,MovieViewSetAdmin

router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='movie')
router.register(r'tickets', TicketViewSet, basename='ticket')

urlpatterns = [
    path('movies/search/<str:moviename>/', MovieViewSet.as_view({'get': 'search'}), name='movie-search'),
    path('all', MovieViewSet.as_view({'get': 'all'}), name='movies'),
    path('<str:moviename>/add/', TicketViewSet.as_view({'post': 'add'}), name='book-ticket'),
    path('tickets/list/', TicketViewSetAdmin.as_view({'get': 'list'}), name='view-tickets-admin'),
    path('<str:moviename>/delete/<int:movie_id>/', MovieViewSetAdmin.as_view({'delete': 'delete_movie'}), name='delete_movie'),
    path('<str:movie_name>/update/<int:movie_id>/', MovieViewSetAdmin.as_view({'put': 'update_seats_available'}), name='update_ticket'),
]
