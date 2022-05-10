from rest_framework import serializers
from imdbproject.movies.models import Movie, Genre, Reaction, Comment

class GenreSerializer(serializers.ModelSerializer):

    id = serializers.ModelField(model_field=Genre()._meta.get_field('id'))
    class Meta:
        model = Genre
        fields = ("id", "name")

class MovieSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    likes = serializers.IntegerField(read_only=True, default=0)
    dislikes = serializers.IntegerField(read_only=True, default=0)
    has_reaction = serializers.IntegerField(read_only=True, default=0)

    def create(self, validated_data):
        
        genres_data = validated_data.pop('genre', [])

        movie = super(MovieSerializer, self).create(validated_data)
        movie_genre_ids = []        
        for genre in genres_data:
            movie_genre_ids.append(genre['id'])

    
        movie_genres = Genre.objects.filter(
           pk__in=movie_genre_ids
        )

        for g in movie_genres:
            movie.genre.add(g)

        return movie


    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'image_url', 'genre', 'num_of_views', 'likes', 'dislikes','has_reaction']


class AddReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ['like']

class AddCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['content']

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'created_at']

class PopularMovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ['id', 'title']

class RelatedSerializes(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ['id', 'title']