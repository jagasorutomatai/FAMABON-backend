from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('household/books', views.BookViewSet)
router.register('household/tags', views.TagViewSet)

app_name = 'apiv1'
urlpatterns = [
    path('', include(router.urls))
]
