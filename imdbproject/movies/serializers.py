from rest_framework import serializers
from imdbproject.movies.models import Movie

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'image_url', 'genre']

