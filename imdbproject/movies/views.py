from django.shortcuts import render
from .models import Like, Movie, Genre, Reaction, Comment, MovieImage
from imdbproject.movies.serializers import MovieSerializer, GenreSerializer, AddReactionSerializer, CommentSerializer, AddCommentSerializer, PopularMovieSerializer, RelatedSerializes
from rest_framework import viewsets
from rest_framework.response import Response
from imdbproject.movies.moviesPagination import MoviesListPagination, CommentListPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.db.models import Q, Count, Sum
from django.db.models.functions import Coalesce
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_201_CREATED
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated


class MovieViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    pagination_class = MoviesListPagination
    Permission_class=[IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title']
    filterset_fields = ['genre']

    queryset = Movie.objects.all()

    def get_queryset(self):
        return Movie.objects.annotate(
            likes=Coalesce(Count('movie_likes__like', filter=Q(movie_likes__like=Like.LIKE)), 0),
            dislikes=Coalesce(Count('movie_likes__like', filter=Q(movie_likes__like=Like.DISLIKE)), 0),
            has_reaction=Coalesce(Count('movie_likes__like', filter=Q(movie_likes__user=self.request.user.id)), 0)
        ).order_by('id')

    def create(self, request):
        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image = MovieImage.objects.create(thumbnail=request.FILES.get('image_url'), full_size=request.FILES.get('image_url'))
        movie = Movie.objects.create(**serializer.data, image_url=image)
        response_serializer = self.get_serializer(movie)
        return Response(response_serializer.data, status=HTTP_201_CREATED)
        
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

    @action(detail=True, url_path='related') 
    def related(self, request, pk):
        movie = self.get_object()          
        queryset = Movie.objects.filter(genre=movie.id).exclude(pk=pk)[:10]
        response_serializer = RelatedSerializes(queryset, many=True)
        return Response(response_serializer.data, status=HTTP_200_OK)

class GenreViewset(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer
    pagination_class = CommentListPagination

    def get_queryset(self):
        return Comment.objects.filter(movie=self.kwargs['movie_pk']).order_by('-created_at')
        
    def create(self, request, movie_pk):
        serializer = AddCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        movie_comment = Comment.objects.create(**serializer.data, movie_id=movie_pk, user=request.user)
        response_serializer = self.get_serializer(movie_comment)
        return Response(response_serializer.data, status=HTTP_201_CREATED)

class PopularMovieViewSet(viewsets.ModelViewSet):

    queryset = Movie.objects.all()
    serializer_class = PopularMovieSerializer

    def list(self, request):
        likesQuery = Coalesce(Count('movie_likes__like', filter=Q(movie_likes__like=Like.LIKE)), 0)
        queryset = Movie.objects.annotate(likes=likesQuery).filter(likes__gt=0).order_by('-likes')[:10]
        response_serializer = PopularMovieSerializer(queryset, many=True)
        return Response(response_serializer.data, status=HTTP_200_OK)
