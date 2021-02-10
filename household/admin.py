from django.contrib import admin

from .models import Book


class BookModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'money', 'date', 'account',
                    'created_at', 'updated_at')
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at', 'updated_at')


admin.site.register(Book, BookModelAdmin)
