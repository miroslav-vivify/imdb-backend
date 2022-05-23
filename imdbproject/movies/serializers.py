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
    thumbnail = serializers.SerializerMethodField()
    full_size = serializers.SerializerMethodField()

    def get_thumbnail(self, obj):
        return obj.image_url.thumbnail.url if obj.image_url is not None else False

    def get_full_size(self, obj):
        return obj.image_url.full_size.url if obj.image_url is not None else False

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'genre', 'image_url', 'num_of_views', 'likes', 'dislikes','has_reaction', 'thumbnail', 'full_size']


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