from django.db.models import Sum
from household.models.book import Book
from household.models.tag import Tag
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import BookFilter
from .serializers import (BookSerializer, PeriodSerializer, TagSerializer,
                          TestSerializer, TotalByDateSerializer,
                          TotalByTagSerializer)

# from rest_framework_simplejwt.authentication import \
#     JWTAuthentication as simplejwt


class BookViewSet(viewsets.ModelViewSet):
    """
    帳簿ViewSet
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = BookFilter

    @action(detail=False)
    def total(self, request):
        """帳簿の合計を返却する"""
        print("===========================================")
        print(request.user)
        print(request.auth)
        date_after = request.GET.get("date_after")
        date_before = request.GET.get("date_before")

        if date_after is not None or date_before is not None:
            total = Book.objects.all().filter(date__range=(
                date_after, date_before)).aggregate(total=Sum("money"))
        else:
            total = Book.objects.all().aggregate(total=Sum("money"))
        serializer = TestSerializer(data=total)
        serializer.is_valid()
        return Response(serializer.data)

    @ action(detail=False)
    def totalByDate(self, request):
        """帳簿の日別の合計一覧を返す"""

        date_after = request.GET.get("date_after")
        date_before = request.GET.get("date_before")
        total_by_date = Book.objects.values("date").annotate(
            total=Sum("money")).order_by("-date").reverse()

        # URLクエリパラメータが存在する場合の処理
        if date_after is not None or date_before is not None:
            total_by_date = total_by_date.filter(
                date__range=(date_after, date_before))
        serializer = TotalByDateSerializer(data=list(total_by_date), many=True)

        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @ action(detail=False)
    def totalByTag(self, request):
        """タグ別の合計一覧を返す"""
        date_after = request.GET.get("date_after")
        date_before = request.GET.get("date_before")
        books = Book.objects.select_related('tag').values(
            "money", "date", "tag__name", "tag__color")

        # URLクエリパラメータが存在する場合の処理
        if date_after is not None or date_before is not None:
            books = books.filter(date__range=(date_after, date_before))
        total_by_tag = books.values(
            "tag__name", "tag__color").annotate(total=Sum("money"))
        serializer = TotalByTagSerializer(data=list(total_by_tag), many=True)

        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    def period(self, request):
        period = Book.objects.values(
            "date").distinct().order_by("-date").reverse()
        serializer = PeriodSerializer(data=list(period), many=True)

        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class TagViewSet(viewsets.ModelViewSet):
    """
    タグViewSet
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
