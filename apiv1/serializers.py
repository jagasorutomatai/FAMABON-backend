from household.models.book import Book
from household.models.tag import Tag
from rest_framework import serializers


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color']


class BookSerializer(serializers.ModelSerializer):
    account = serializers.ReadOnlyField(source='account.username')
    tag = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'money', 'date', 'tag',
                  'account', 'created_at', 'updated_at']
