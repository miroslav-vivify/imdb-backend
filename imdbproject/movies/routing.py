from django.urls import re_path

from imdbproject.movies import consumers

websocket_urlpatterns = [
    re_path(r'ws/movies/(?P<id>\w+)$', consumers.MovieEventConsumer.as_asgi()),
]
