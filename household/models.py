import uuid

from account.models import Account
from django.db import models


class Book(models.Model):
    """帳簿モデル"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(verbose_name='タイトル', max_length=50)
    money = models.IntegerField(verbose_name='金額')
    date = models.DateTimeField(verbose_name='日付')
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name='登録日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)

    def __str__(self):
        return self.title
