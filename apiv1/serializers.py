from household.models import Book
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'money', 'date',
                  'account', 'created_at', 'updated_at']
