from django.contrib import admin

from .models.book import Book
from .models.tag import Tag


class BookModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'money', 'date', 'account',
                    'created_at', 'updated_at')
    ordering = ('-created_at',)
    readonly_fields = ('uuid', 'created_at', 'updated_at')


class TagModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'account', 'created_at', 'updated_at')
    ordering = ('-updated_at',)
    readonly_fields = ('uuid', 'created_at', 'updated_at')


admin.site.register(Book, BookModelAdmin)
admin.site.register(Tag, TagModelAdmin)
