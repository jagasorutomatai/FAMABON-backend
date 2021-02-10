import uuid

from django.db import models


class Tag(models.Model):
    """
    帳簿分別用タグモデル
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name='タグの名前', max_length=50)
    created_at = models.DateTimeField(verbose_name='登録日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)

    class Meta:
        app_label = 'household'

    def __str__(self):
        return self.name
