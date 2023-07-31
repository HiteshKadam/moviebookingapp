from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from movies.models import Movie, Ticket
from movies.serializers import MovieSerializer, TicketSerializer

class MovieViewSetTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='admin', password='admin')
        self.movie1 = Movie.objects.create(movie_name='Movie 1', theatre_name='Theatre 1', total_tickets_allotted=100)
        self.movie2 = Movie.objects.create(movie_name='Movie 2', theatre_name='Theatre 2', total_tickets_allotted=50)

    def test_all_movies(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('movies'))
        self.assertEqual(response.status_code, 200)
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        self.assertEqual(response.json(), serializer.data)

    def test_search_movie_existing(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('movie-search', args=['Movie 1']))
        self.assertEqual(response.status_code, 200)
        movies = Movie.objects.filter(movie_name__icontains='Movie 1')
        serializer = MovieSerializer(movies, many=True)
        self.assertEqual(response.json(), serializer.data)

    def test_search_movie_nonexistent(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('movie-search', args=['Movie 3']))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'message': 'Movie does not exist.'})

class TicketViewSetTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='admin', password='admin')
        self.movie1 = Movie.objects.create(movie_name='Movie 1', theatre_name='Theatre 1', total_tickets_allotted=100)
        self.movie2 = Movie.objects.create(movie_name='Movie 2', theatre_name='Theatre 2', total_tickets_allotted=50)

    def test_add_ticket_success(self):
        self.client.force_login(self.user)
        url = reverse('book-ticket', args=['Movie 1'])
        data = {'num_tickets': 3}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        ticket = Ticket.objects.latest('id')
        movie_serializer = MovieSerializer(ticket.movie)
        ticket_serializer = TicketSerializer(ticket)
        expected_data = {
            'movie': movie_serializer.data,
            'ticket': ticket_serializer.data
        }
        self.assertEqual(response.json(), expected_data)

    def test_add_ticket_insufficient_tickets(self):
        self.client.force_login(self.user)
        url = reverse('book-ticket', args=['Movie 2'])
        data = {'num_tickets': 100}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'Not enough tickets available for booking.'})

    # def test_list_tickets(self):
    #     self.client.force_login(self.user)
    #     url = reverse('view-tickets')
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 403)  # Adjusted expected status code to 403 (Forbidden)

class MovieViewSetAdminTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(username='admin', password='admin')
        self.movie1 = Movie.objects.create(movie_name='Movie 1', theatre_name='Theatre 1', total_tickets_allotted=100)
        self.movie2 = Movie.objects.create(movie_name='Movie 2', theatre_name='Theatre 2', total_tickets_allotted=50)

    def test_delete_movie(self):
        self.client.force_login(self.admin)
        url = reverse('delete_movie', args=['Movie 1', self.movie1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Movie.objects.filter(id=self.movie1.id).exists())
        self.assertFalse(Ticket.objects.filter(movie=self.movie1).exists())

    def test_delete_movie_nonexistent(self):
        self.client.force_login(self.admin)
        url = reverse('delete_movie', args=['Movie 3', 99])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'detail': 'Not found.'})