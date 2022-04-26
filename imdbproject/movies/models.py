from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Like(models.IntegerChoices):
    LIKE = 1
    DISLIKE = -1

class Genre(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
        
class Movie(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
    image_url = models.TextField()
    genre = models.ManyToManyField(Genre)
    num_of_views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Reaction(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')
    like = models.IntegerField(choices=Like.choices)

    class Meta:
        unique_together = ('movie', 'user',)

    def __str__(self):
        return f'{self.movie} | {self.user}'