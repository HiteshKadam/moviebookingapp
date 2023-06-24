from django.test import TestCase
from django.core.exceptions import ValidationError
from movies.models import Movie, Ticket

class MovieModelTest(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(movie_name='Movie 1', theatre_name='Theatre 1', total_tickets_allotted=100)

    def test_movie_creation(self):
        self.assertEqual(self.movie.movie_name, 'Movie 1')
        self.assertEqual(self.movie.theatre_name, 'Theatre 1')
        self.assertEqual(self.movie.total_tickets_allotted, 100)

class TicketModelTest(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(movie_name='Movie 1', theatre_name='Theatre 1', total_tickets_allotted=100)
        self.ticket = Ticket.objects.create(movie=self.movie, num_tickets=2, seat_number='A1')

    def test_ticket_creation(self):
        self.assertEqual(self.ticket.movie, self.movie)
        self.assertEqual(self.ticket.num_tickets, 2)
        self.assertEqual(self.ticket.seat_number, 'A1')

    def test_movie_cascade_deletion(self):
        self.movie.delete()
        self.assertEqual(Ticket.objects.count(), 0)

    def test_movie_foreign_key_constraint(self):
        with self.assertRaises(ValidationError) as context:
            ticket = Ticket(movie=None, num_tickets=2, seat_number='A2')
            ticket.full_clean()
        self.assertEqual(context.exception.message_dict['movie'][0], 'This field cannot be null.')

    def test_num_tickets_positive_value(self):
        ticket = Ticket(movie=self.movie, num_tickets=-1, seat_number='A2')
        with self.assertRaises(ValidationError) as context:
            ticket.clean_fields(exclude=['movie'])
        self.assertEqual(
            context.exception.message_dict['num_tickets'][0],
            'Ensure this value is greater than or equal to 0.'
        )

    def test_seat_number_length(self):
        ticket = Ticket(movie=self.movie, num_tickets=2, seat_number='A1wfewewf2B3')
        with self.assertRaises(ValidationError) as context:
            ticket.clean_fields(exclude=['movie'])
        self.assertEqual(
            context.exception.message_dict['seat_number'][0],
            'Ensure this value has at most 10 characters.'
        )

    def test_ticket_model_str_representation(self):
        self.assertEqual(str(self.ticket), f"Ticket object (8)")

    def test_total_tickets_available(self):
        tickets_sold = Ticket.objects.filter(movie=self.movie).count()
        available_tickets = self.movie.total_tickets_allotted - tickets_sold
        self.assertEqual(self.get_total_tickets_available(), available_tickets)

    def test_ticket_decrement_on_save(self):
        initial_tickets = self.get_total_tickets_available()
        new_ticket = Ticket(movie=self.movie, num_tickets=1, seat_number='A2')
        new_ticket.save()
        updated_tickets = self.get_total_tickets_available()
        self.assertEqual(updated_tickets, initial_tickets - new_ticket.num_tickets)

    def get_total_tickets_available(self):
        tickets_sold = Ticket.objects.filter(movie=self.movie).count()
        return self.movie.total_tickets_allotted - tickets_sold