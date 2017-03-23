from celery import task
from django.conf import settings
from pusher import Pusher
from appcinema.api.models import Movie


@task(ignore_result=True)
def destroy_tentative_seat(movie_pk, seat_id):
    movie = Movie.objects.get(pk=movie_pk)
    try:
        movie.tentative_booked.remove(seat_id)
    except Exception:
        pass
    movie.save()
    channel = u"movie_%s" % movie_pk

    pusher = Pusher(app_id=settings.PUSHER_APP_ID,
                    key=settings.PUSHER_KEY,
                    secret=settings.PUSHER_SECRET,
                    cluster=settings.PUSHER_CLUSTER)
    pusher.trigger(
        [channel, ],
        'destroy_tentative_seat',
        {
            'seat_id': seat_id,
        }
    )


@task
def tentative_to_booked(movie_pk, seats):
    seats = eval(seats)
    movie = Movie.objects.get(pk=movie_pk)
    movie.tentative_booked = [x for x in movie.tentative_booked if x not in seats]
    movie.booked_seats.extend(seats)
    movie.save()
    channel = u"movie_%s" % movie_pk

    pusher = Pusher(app_id=settings.PUSHER_APP_ID,
                    key=settings.PUSHER_KEY,
                    secret=settings.PUSHER_SECRET,
                    cluster=settings.PUSHER_CLUSTER)
    pusher.trigger(
        [channel, ],
        'tentative_to_booked',
        {
            'seats': seats,
        }
    )
