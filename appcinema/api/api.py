from rest_framework import generics, permissions

from .serializers import MovieSerializer
from .models import Movie


class MovieDetail(generics.RetrieveAPIView):
    model = Movie
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = 'id'


class MovieList(generics.ListCreateAPIView):
    model = Movie
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    permission_classes = [
        permissions.AllowAny
    ]

