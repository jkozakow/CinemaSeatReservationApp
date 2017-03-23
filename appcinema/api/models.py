from django.db import models

from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


class Movie(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateTimeField()
    booked_seats = ArrayField(base_field=models.IntegerField(), null=True, blank=True)
    tentative_booked = ArrayField(base_field=models.IntegerField(), null=True, blank=True)

    class Meta:
        db_table = 'movies'

    def __str__(self):
        return '%s %s' % (self.name, self.date.strftime('%d/%m/%y %H:%M'))


class Booking(models.Model):
    movie = models.ForeignKey(Movie)
    user = models.ForeignKey(User)
    seats = ArrayField(base_field=models.IntegerField(), size=5)

    class Meta:
        db_table = 'bookings'
