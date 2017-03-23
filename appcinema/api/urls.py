from django.conf.urls import url, include

from .api import MovieList, MovieDetail

movie_urls = [
    url(r'^/$', MovieList.as_view(), name='movies-list'),
    url(r'^/(?P<movie_id>[0-9]+)$', MovieDetail.as_view(), name='movie-detail'),
]

urlpatterns = [
    url(r'^movies', include(movie_urls)),
]
