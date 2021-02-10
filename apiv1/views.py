from household.models import Book
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    帳簿モデルのREST API
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
