from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from .models import Movie, Ticket
from .serializers import MovieSerializer, TicketSerializer
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.db.models import Sum
import logging as log
from kafka import KafkaProducer
from kafka.errors import KafkaError

logger = log.getLogger(__name__)
KAFKA_TOPIC = 'DeleteMovieRequested'
KAFKA_SERVER = 'localhost:9092'

class MovieViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def all(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return JsonResponse(serializer.data, safe=False)

    @action(detail=False, methods=['get'])
    def search(self, request,**kwargs):
        movie_name = str(kwargs['moviename'])
        movies = Movie.objects.filter(movie_name__icontains=movie_name)
        serializer = MovieSerializer(movies, many=True)
        logger.info('Movie Searched Published!')
        return JsonResponse(serializer.data, safe=False)

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    @action(detail=False, methods=['post'])
    def add(self, request, moviename=None):
        try:
            movie = Movie.objects.get(movie_name=moviename)
            num_tickets = request.data.get('num_tickets')
            logger.info('%s',movie)
            if int(num_tickets) <= movie.total_tickets_allotted:
                # If we automate the seat updating
                # movie.total_tickets_allotted -= int(num_tickets)
                # movie.save()
                ticket = Ticket(movie=movie, num_tickets=num_tickets)
                ticket.save()
                movie_serializer = MovieSerializer(movie)
                ticket_serializer = TicketSerializer(ticket)
                response_data = {
                    'movie': movie_serializer.data,
                    'ticket': ticket_serializer.data
                }
                logger.info('Ticket Booked Published!')
                return JsonResponse(response_data)
            else:
                return JsonResponse({'message': 'Not enough tickets available for booking.'}, status=400)
        except Movie.DoesNotExist:
            logger.error('Movie Does not exist error!')
            return JsonResponse({'message': 'Movie does not exist.'}, status=404)

    def list(self, request):
        tickets = Ticket.objects.aggregate.filter(user=request.user)  # Filter tickets by the logged-in user
        serializer = TicketSerializer(tickets, many=True)
        return JsonResponse(serializer.data, safe=False)

class TicketViewSetAdmin(viewsets.ViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAdminUser]  # Ensure only admin users can access this viewset

    def list(self, request):
        tickets = Ticket.objects.all()
        serializer = TicketSerializer(tickets, many=True)
        return JsonResponse(serializer.data, safe=False)


class MovieViewSetAdmin(viewsets.ViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAdminUser]  # Ensure only admin users can access this viewset

    @action(detail=False, methods=['put'])
    def update_seats_available(self, request,movie_name=None,movie_id=None):

        movie = get_object_or_404(Movie, id=movie_id)
        movie_id = movie_id
        movie_name = movie.movie_name
        tickets = Ticket.objects.filter(movie=movie_id)

        total_tickets_booked = tickets.aggregate(total=Sum('num_tickets'))['total']
        total_tickets_booked = total_tickets_booked if total_tickets_booked else 0

        seats_available = movie.total_tickets_allotted - total_tickets_booked
        seats_available = seats_available if seats_available >= 0 else 0

        if seats_available == 0:
            status = 'SOLD OUT'
        else:
            status = 'BOOK ASAP'
        logger.info('Tickets Status: %s',status)

        movie.total_tickets_allotted = seats_available
        movie.save()
        logger.info('Movie Updated!')
        response_data = {
            'message': f'Successfully updated seats available for movie "{movie_name}"',
            'seats_available': seats_available,
            'ticket_status': status
        }
        return JsonResponse(response_data)

    @action(detail=False, methods=['delete'])
    def delete_movie(self, request, moviename=None, movie_id=None):
        movie = get_object_or_404(Movie, id=movie_id)
        movie_name = movie.movie_name

        # Delete all associated tickets
        tickets = Ticket.objects.filter(movie=movie)
        tickets.delete()
        logger.info('Tickets Deleted!')

        # Delete the movie
        movie.delete()
        logger.info('Movie Deleted!')
        send_message(movie_name)
        
        return JsonResponse({'message': f'Movie "{movie_name}" and associated tickets have been deleted successfully.'})


def send_message(movie_name):
    producer = KafkaProducer(bootstrap_servers=[KAFKA_SERVER])
    response = 'Movie "{}" has been deleted.'.format(movie_name)
    future = producer.send(KAFKA_TOPIC, bytes(response, 'utf-8'))

    try:
        record_metadata = future.get(timeout=10)
        print('Message sent successfully!', record_metadata.topic, record_metadata.partition, record_metadata.offset)
    except KafkaError as e:
        print('Failed to send message to Kafka:', e)
    finally:
        producer.flush()

'''
Handy server commands kafka

zookeeper-server-start.bat ..\..\config\zookeeper.properties

kafka-server-start.bat ..\..\config\server.properties'''