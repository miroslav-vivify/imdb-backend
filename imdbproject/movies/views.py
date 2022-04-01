from django.shortcuts import render
from .models import Movie, Genre
from imdbproject.movies.serializers import MovieSerializer, GenreSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from imdbproject.movies.moviesPagination import MoviesListPagination
from rest_framework import filters



class MovieViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    pagination_class = MoviesListPagination

    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    
    queryset = Movie.objects.all() 

    def create(self, request):
        movie_data = request.data

        new_movie = MovieSerializer(data=movie_data)
        if not new_movie.is_valid():
            return Response(new_movie._errors, 400)
        new_movie.save()   

        return Response(movie_data, 200)

class GenreViewset(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
