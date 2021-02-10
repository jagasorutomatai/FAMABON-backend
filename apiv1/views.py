from household.models.book import Book
from household.models.tag import Tag
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import BookSerializer, TagSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    帳簿モデルのREST API
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class TagViewSet(viewsets.ModelViewSet):
    """
    帳簿分割用タグのREST API
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
