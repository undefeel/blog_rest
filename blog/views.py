from .models import BlogModel
from .serializers import BlogSerializer

from rest_framework import viewsets


class BlogView(viewsets.ModelViewSet):
    queryset = BlogModel.objects.all()
    serializer_class = BlogSerializer