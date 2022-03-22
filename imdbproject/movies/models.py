from django.db import models
from .utils import MOVIE_GENRES

class Movie(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
    image_url = models.TextField()
    genre = models.CharField(max_length=30, choices=MOVIE_GENRES, default=MOVIE_GENRES.horror)

    def __str__(self):
        return self.title
