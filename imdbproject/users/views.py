from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.decorators import action
from .serializers import CreateUserSerializer, UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, TokenObtainPairSerializer

User = get_user_model()

class UserViewSet(mixins.CreateModelMixin,
                viewsets.GenericViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        return UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        User.objects.create_user(**serializer.data)
        return Response(status=HTTP_201_CREATED)

    @action(detail=False, url_path='me', permission_classes=[IsAuthenticated]) 
    def get_current_user(self, request):          
        response_serializer = UserSerializer(request.user)
        return Response(response_serializer.data, HTTP_200_OK)

class RegisterView(APIView):
    http_method_names = ['post']

    def post(self, *args, **kwargs):
        serializer = UserSerializer(data=self.request.data)
        if serializer.is_valid():
            get_user_model().objects.create_user(**serializer.validated_data)
            return Response(status=HTTP_201_CREATED)
        return Response(status=HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer