from django_filters import rest_framework as filters
from household.models.book import Book
from household.models.tag import Tag
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .filters import BookFilter
from .serializers import BookSerializer, TagSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    帳簿ViewSet
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = BookFilter


class TagViewSet(viewsets.ModelViewSet):
    """
    タグViewSet
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
