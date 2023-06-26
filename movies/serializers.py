from rest_framework import serializers
from .models import Movie, Ticket

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'movie_name', 'theatre_name', 'total_tickets_allotted']

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'movie', 'num_tickets', 'seat_number']

class TicketSerializerMovieName(serializers.ModelSerializer):
    movie = MovieSerializer()  # Nested serializer for movie
    class Meta:
        model = Ticket
        fields = ['id', 'movie', 'num_tickets', 'seat_number']
