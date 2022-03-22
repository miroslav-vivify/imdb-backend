from django.urls import path
from rest_framework import routers
from imdbproject.users.views import UserViewSet
from rest_framework_simplejwt.views import TokenRefreshView
from imdbproject.users.views import EmailTokenObtainPairView, RegisterView

userRouter = routers.SimpleRouter()
userRouter.register(r'', UserViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='token_obtain_pair'),
    path('login/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] 