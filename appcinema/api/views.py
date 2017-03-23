from django.views.generic import DetailView, ListView
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import get_user

from pusher import Pusher

from .models import Movie, Booking
from .tasks import destroy_tentative_seat, tentative_to_booked


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movie_detail.html'


def add_tentative_seat(request, movie_pk, seat_id):
    channel = u"movie_%s" % movie_pk

    pusher = Pusher(app_id=settings.PUSHER_APP_ID,
                    key=settings.PUSHER_KEY,
                    secret=settings.PUSHER_SECRET,
                    cluster=settings.PUSHER_CLUSTER)
    pusher.trigger(
        [channel, ],
        'add_tentative_seat',
        {
            'seat_id': seat_id,
        }
    )
    movie = Movie.objects.get(pk=movie_pk)
    movie.tentative_booked.append(seat_id)
    movie.save()
    destroy_tentative_seat.apply_async((movie_pk, int(seat_id)), countdown=settings.FREE_TENTATIVE_BOOKED_TIME)
    return HttpResponse('')


def booking_create_view(request):
    seats_data = request.POST.get('booking_seats')
    seats = seats_data.split(",")
    seat_ids = []

    for seat in seats:
        seat_ids.append(''.join(filter(lambda x: x.isdigit(), seat)))

    context = {
        'seats': list(map(int, seat_ids)),
        'movie': request.POST.get('movie'),
        'movie_id': request.POST.get('movie_id')
    }
    return render(request, 'booking_create.html', context)


def confirm_booking(request):
    seats = request.POST['seats']
    movie_id = request.POST['movie_id']
    booking = Booking.objects.create(seats=eval(seats),
                                     movie_id=movie_id,
                                     user=get_user(request))
    booking.save()
    tentative_to_booked.apply_async((movie_id, seats), countdown=settings.BOOK_DELAY_AFTER_CONFIRM_TIME)

    return render(request, 'booking_success.html', {})


class BookingHistoryView(ListView):
    model = Booking
    template_name = 'booking_history.html'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
