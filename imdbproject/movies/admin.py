from django.contrib import admin
from .models import Movie, Genre, Reaction, Comment, MovieImage

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Reaction)
admin.site.register(Comment)
admin.site.register(MovieImage)
