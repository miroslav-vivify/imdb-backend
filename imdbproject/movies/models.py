from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
        
class Movie(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
    image_url = models.TextField()
    genre = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title
