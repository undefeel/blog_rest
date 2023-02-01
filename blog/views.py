from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from .models import BlogModel
from .serializers import BlogSerializer, UserSerializer

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.settings import DEFAULTS


class UserView(CreateAPIView):
    model = get_user_model()
    
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        user = User.objects.create_user(**request.data)
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
            })


class BlogView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = BlogModel.objects.all()
    
    def create(self, request, *args, **kwargs):
        
        header = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        token = TokenBackend(algorithm='HS256', signing_key= DEFAULTS['SIGNING_KEY']).decode(header, verify=True)
        request.data['owner'] = token['user_id']
        print(request.data)
        return super().create(request, *args, **kwargs)
        # return Response(request.data)
    serializer_class = BlogSerializer