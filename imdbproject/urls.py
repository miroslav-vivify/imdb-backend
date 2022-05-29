"""imdbproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from imdbproject.users.views import EmailTokenObtainPairView, UserViewSet, WatchlistViewSet, RegisterView
from imdbproject.movies.views import CommentViewSet, MovieViewSet, GenreViewset, PopularMovieViewSet
from rest_framework_nested import routers

router_movie = routers.DefaultRouter()
router_movie.register(r'api/movies', MovieViewSet, basename='movie')

router_comment = routers.NestedSimpleRouter(router_movie, r'api/movies', lookup='movie')
router_comment.register(r'comments', CommentViewSet, basename='comments')

router_genres = routers.SimpleRouter()
router_genres.register(r'api/genres', GenreViewset, basename='genre')

router_popular_movies = routers.SimpleRouter()
router_popular_movies.register(r'api/popular', PopularMovieViewSet, basename='popular')

router_user = routers.SimpleRouter()
router_user.register(r'api/users', UserViewSet, basename='user')

router_watchlist = routers.SimpleRouter()
router_watchlist.register(r'api/watchlist', WatchlistViewSet, basename='watchlist')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view(), name='token_obtain_pair'),
    path('login/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', include(router_user.urls)),
    path('', include(router_movie.urls)),
    path('', include(router_comment.urls)),
    path('', include(router_genres.urls)),
    path('', include(router_popular_movies.urls)), 
    path('', include(router_watchlist.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
