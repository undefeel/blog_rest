from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import BlogModel, CommentModel


class BlogSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BlogModel
        fields = ['title', 'text', 'owner']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ['comment', 'blog', 'owner']