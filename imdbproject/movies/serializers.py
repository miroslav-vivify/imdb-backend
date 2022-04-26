from rest_framework import serializers
from imdbproject.movies.models import Movie, Genre, Reaction

class GenreSerializer(serializers.ModelSerializer):

    id = serializers.ModelField(model_field=Genre()._meta.get_field('id'))
    class Meta:
        model = Genre
        fields = ("id", "name")

class MovieSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    likes = serializers.IntegerField(read_only=True, default=0)
    dislikes = serializers.IntegerField(read_only=True, default=0)
    liked_or_disliked_user = serializers.IntegerField(read_only=True, default=0)

    def create(self, validated_data):
        
        genres_data = validated_data.pop('genre', [])

        movie = super(MovieSerializer, self).create(validated_data)
        movie_genre_ids = []        
        for genre in genres_data:
            movie_genre_ids.append(genre['id'])

        # print(movie_genre_ids)

        movie_genres = Genre.objects.filter(
           pk__in=movie_genre_ids
        )

        for g in movie_genres:
            movie.genre.add(g)

        #movie.genre.add(*[movie_genres])
        return movie


    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'image_url', 'genre', 'num_of_views', 'likes', 'dislikes','liked_or_disliked_user']


class AddReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ['like']
