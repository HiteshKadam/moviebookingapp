from django.db import models

class Movie(models.Model):
    movie_name = models.CharField(max_length=100)
    theatre_name = models.CharField(max_length=100)
    total_tickets_allotted = models.IntegerField()

class Ticket(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    num_tickets = models.IntegerField()
    seat_number = models.CharField(max_length=10)
