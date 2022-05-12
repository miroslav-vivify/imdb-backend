from django.db import models
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models.signals import post_save

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

def movie_post_save(sender, instance, created, *args, **kwargs):
    if created:
        send_mail(
            'A new movie is added to the system.: {}'.format(instance.title),
            'Title: {}\nDescription: {}'.format(
                instance.title, instance.description),
            'from@example.com',
            ['miroslav.cvijanovic@vivifyideas.com'],
            fail_silently=False,
        )
        
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
