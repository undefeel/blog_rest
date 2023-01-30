from django.contrib import admin
from django.urls import path

from rest_framework_swagger.views import get_swagger_view
from rest_framework.routers import DefaultRouter

from blog.views import BlogView


swagger_view = get_swagger_view(title='Test')

router = DefaultRouter()
router.register(r'blogs', BlogView, basename='blogs')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', swagger_view)
]

urlpatterns += router.urls
