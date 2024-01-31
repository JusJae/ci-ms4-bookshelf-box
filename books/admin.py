from django.contrib import admin
from .models import Book, Category


class BookAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'category',
        'rating',
        'price',
        'availability',
        'reviews',
    )

    ordering = ('id',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'category',
    )

    ordering = ('category',)


admin.site.register(Book, BookAdmin)
admin.site.register(Category, CategoryAdmin)
