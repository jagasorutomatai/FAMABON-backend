import uuid

from account.models import Account
from django.db import models


class Tag(models.Model):
    """
    帳簿分別用タグモデル
    """

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name='タグの名前', max_length=50)
    color = models.CharField(
        verbose_name='タグの色', max_length=20, default='grey')
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name='登録日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)

    class Meta:
        app_label = 'household'

    def __str__(self):
        return self.name
