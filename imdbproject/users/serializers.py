from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as JwtTokenObtainPairSerializer
from imdbproject.users.models import CustomUser
from imdbproject.movies.models import MovieWatchList, Movie
from imdbproject.movies.serializers import BasicMovieSerializer
from django.contrib.auth import get_user_model

User = get_user_model()
    
class TokenObtainPairSerializer(JwtTokenObtainPairSerializer):
    username_field = CustomUser.USERNAME_FIELD

class MovieWatchlistSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all(), read_only=False)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['movie_object'] = BasicMovieSerializer(instance.movie).data
        return rep

    class Meta:
        model = MovieWatchList
        fields = ['id', 'movie', 'is_watched', 'user', ]

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'name']
    
    name = serializers.CharField(required=True)

class UserSerializer(serializers.ModelSerializer):
    user_watchlist = MovieWatchlistSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'name', 'user_watchlist', ]
