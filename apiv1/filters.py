from django_filters import rest_framework as filters
from household.models.book import Book


class BookFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='contains')
    date = filters.DateFromToRangeFilter(field_name='date')
    tag = filters.CharFilter(field_name="tag__name", lookup_expr='contains')

    class Meta:
        model = Book
        fields = ['title', 'date']
