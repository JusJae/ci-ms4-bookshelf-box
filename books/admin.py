from django.contrib import admin
from .models import Book, Category


class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'rating',
        'price',
        'availability',
        'reviews',
    )

    ordering = ('title',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'category',
    )

    ordering = ('category',)


admin.site.register(Book, BookAdmin)
admin.site.register(Category, CategoryAdmin)
