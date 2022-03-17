from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView
from imdbproject.users.api.views import EmailTokenObtainPairView, RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='token_obtain_pair'),
    path('login/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] 