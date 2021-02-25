import uuid

from account.models import Account
from django.db import models
from household.models.tag import Tag


class Book(models.Model):
    """
    帳簿モデル
    """

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(verbose_name='タイトル', max_length=50)
    description = models.TextField(
        verbose_name='説明', null=True, blank=True, max_length=250)
    money = models.IntegerField(verbose_name='金額')
    date = models.DateField(verbose_name='日付')
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE)
    tag = models.ForeignKey(
        Tag, related_name='books', on_delete=models.PROTECT)
    created_at = models.DateTimeField(verbose_name='登録日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)

    class Meta:
        app_label = 'household'

    def __str__(self):
        return self.title
