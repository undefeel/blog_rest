from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from core.models import BaseModel


class BlogModel(BaseModel):
    title = models.CharField(max_length=150)
    text = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.title


class CommentModel(BaseModel):
    name = models.CharField(max_length=100)
    comment = models.TextField()
    blog =  models.ForeignKey('BlogModel', related_name='blog', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.name