from django.shortcuts import render
from .models import Like, Movie, Genre, Reaction
from imdbproject.movies.serializers import MovieSerializer, GenreSerializer, AddReactionSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from imdbproject.movies.moviesPagination import MoviesListPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.db.models import Q, Count, Sum
from django.db.models.functions import Coalesce
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.decorators import action


class MovieViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    pagination_class = MoviesListPagination
    
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title']
    filterset_fields = ['genre']

    queryset = Movie.objects.all()

    def get_queryset(self):
        return Movie.objects.annotate(
            likes=Coalesce(Count('movie_likes__like', filter=Q(movie_likes__like=Like.LIKE)), 0),
            dislikes=Coalesce(Count('movie_likes__like', filter=Q(movie_likes__like=Like.DISLIKE)), 0),
            liked_or_disliked_user=Coalesce(Count('movie_likes__like', filter=Q(movie_likes__user=self.request.user.id)), 0)
        ).order_by('id')

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

    @action(methods=['POST'], detail=True, url_path='like')
    def like(self, request, pk):
        serializer = AddReactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        Reaction.objects.update_or_create(movie=self.get_object(), user=request.user, defaults={**serializer.data})
        return Response(status=HTTP_200_OK)

    @action(methods=['DELETE'], detail=True, url_path='delete-like')
    def delete_like(self, request, pk):
        movie_likes = Reaction.objects.filter(movie_id=pk, user=request.user)
        if not movie_likes.exists():
            error = {"not_exists_error": ["There is no like/dislike for the selected movie and user"]}
            return Response(error, status=HTTP_404_NOT_FOUND)
        movie_likes.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class GenreViewset(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
