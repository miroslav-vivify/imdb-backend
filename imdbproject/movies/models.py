from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from .tasks import send_mail_celery
from easy_thumbnails.fields import ThumbnailerImageField

User = get_user_model()

class MovieImage(models.Model):
    thumbnail = ThumbnailerImageField(
        upload_to='static/thumbnails/', blank=True, null=True, resize_source=dict(size=(200, 200)))
    full_size = ThumbnailerImageField(
        upload_to='static/full-size/', blank=True, null=True, resize_source=dict(size=(400, 400)))

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
    image_url = models.OneToOneField(MovieImage, on_delete=models.CASCADE, blank=True, null=True)
    genre = models.ManyToManyField(Genre)
    num_of_views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

def movie_post_save(sender, instance, created, *args, **kwargs):
    if created:
        send_mail_celery.delay(
            {'title': instance.title, 'description': instance.description})
        
post_save.connect(movie_post_save, sender=Movie)


class Reaction(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')
    like = models.IntegerField(choices=Like.choices)

    class Meta:
        unique_together = ('movie', 'user',)

    def __str__(self):
        return f'{self.movie} | {self.user}'

class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.movie} | {self.user}'
