from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from .models import BlogModel
from .serializers import BlogSerializer, UserSerializer

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import CreateAPIView



class UserView(CreateAPIView):
    model = get_user_model()
    
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        user = User.objects.create_user(**request.data)
        refresh = RefreshToken.for_user(user)
        print(refresh)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
            })


class BlogView(viewsets.ModelViewSet):
    queryset = BlogModel.objects.all()
    serializer_class = BlogSerializer