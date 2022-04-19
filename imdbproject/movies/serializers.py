from rest_framework import serializers
from imdbproject.movies.models import Movie, Genre

class GenreSerializer(serializers.ModelSerializer):

    id = serializers.ModelField(model_field=Genre()._meta.get_field('id'))
    class Meta:
        model = Genre
        fields = ("id", "name")

class MovieSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)

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
        fields = ['id', 'title', 'description', 'image_url', 'genre', 'num_of_views']
