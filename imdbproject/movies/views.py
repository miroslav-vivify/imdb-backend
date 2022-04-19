from django.shortcuts import render

from .models import Movie, Genre
from imdbproject.movies.serializers import MovieSerializer, GenreSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from imdbproject.movies.moviesPagination import MoviesListPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response


class MovieViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    pagination_class = MoviesListPagination
    
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title']
    filterset_fields = ['genre']

    queryset = Movie.objects.all()

    def create(self, request):
        movie_data = request.data

        new_movie = MovieSerializer(data=movie_data)
        if not new_movie.is_valid():
            return Response(new_movie._errors, 400)
        new_movie.save()   

        return Response(None, 200)  

    def retrieve(self, request, pk):
        instance = self.get_object()
        instance.num_of_views += 1
        instance.save()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance)
        return Response(serializer.data)

class GenreViewset(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
