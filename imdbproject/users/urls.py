from django.urls import path
from rest_framework import routers
from imdbproject.users.views import UserViewSet

userRouter = routers.SimpleRouter()
userRouter.register(r'', UserViewSet)
