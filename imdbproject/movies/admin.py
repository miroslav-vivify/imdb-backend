from django.contrib import admin
from .models import Movie, Genre, Reaction, Comment, MovieImages

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Reaction)
admin.site.register(Comment)
admin.site.register(MovieImages)
