from django.shortcuts import render
from rest_framework import generics
from .models import Movie
from imdbproject.movies.serializers import MovieSerializer

class MovieListCreate(generics.CreateAPIView):
    serializer_class = MovieSerializer

    def post(self, request):
        return self.create(request)
    
class MoviesListShow(generics.ListAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()

    def get(self, request):
        return self.list(request)

