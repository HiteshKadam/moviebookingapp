from django.db import models

class Movie(models.Model):
    movie_name = models.CharField(max_length=100)
    theatre_name = models.CharField(max_length=100)
    total_tickets_allotted = models.PositiveIntegerField()

class Ticket(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    num_tickets = models.PositiveIntegerField()
    seat_number = models.CharField(max_length=10, error_messages ={
                    "max_length":"Ensure this value has at most 10 characters."
                    })