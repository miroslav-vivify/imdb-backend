from django.shortcuts import render
from rest_framework import generics
from .models import Movie
from imdbproject.movies.serializers import MovieSerializer


class MovieListCreate(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    
class MoviesListShow(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
