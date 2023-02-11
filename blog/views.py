from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from .models import BlogModel, CommentModel
from .serializers import BlogSerializer, UserSerializer, CommentSerializer

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.settings import DEFAULTS
from rest_framework import status
from core.permissions import IsOwnerOrReadOnly



class UserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        try:
            user = User.objects.create_user(**request.data)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
                })
        except IntegrityError:
            return Response({'Error': 'user already exist'}, status=status.HTTP_409_CONFLICT)


class BlogView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = BlogModel.objects.all()
    serializer_class = BlogSerializer
    
    def create(self, request, *args, **kwargs):
        header = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        token = TokenBackend(algorithm='HS256', signing_key= DEFAULTS['SIGNING_KEY']).decode(header, verify=True)
        request.data['owner'] = token['user_id']
        return super().create(request, *args, **kwargs)


class CommentView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = CommentModel.objects.all()
    serializer_class = CommentSerializer
    
    def create(self, request, *args, **kwargs):
        print(request.data)
        if request.data['csrfmiddlewaretoken']:
            return super().create(request, *args, **kwargs)
        else:
            header = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            token = TokenBackend(algorithm='HS256', signing_key= DEFAULTS['SIGNING_KEY']).decode(header, verify=True)
            request.data['owner'] = token['user_id']
            return super().create(request, *args, **kwargs)
