from django.contrib import admin
from django.urls import path

from rest_framework_swagger.views import get_swagger_view
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)


from blog.views import BlogView, UserView, CommentView


swagger_view = get_swagger_view(title='Test')

router = DefaultRouter()
router.register(r'blogs', BlogView, basename='blogs')
router.register(r'comments', CommentView, basename='comments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', swagger_view),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('users/', UserView.as_view())
]

urlpatterns += router.urls
