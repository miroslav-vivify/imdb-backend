from django.shortcuts import render
from rest_framework import generics
from .models import Movie
from imdbproject.movies.serializers import MovieSerializer


class MovieListCreate(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    
class MoviesListShow(generics.ListAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()

    def get(self, request):
        return self.list(request)

    
