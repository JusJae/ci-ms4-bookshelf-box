from django.contrib import admin
from .models import SubscriptionOption


class SubscriptionOptionAdmin(admin.ModelAdmin):
    list_display = ('category', 'number_of_books', 'subscription_type', 'price')  # noqa
    list_filter = ('category', 'subscription_type')
    search_fields = ('category', 'subscription_type')


admin.site.register(SubscriptionOption, SubscriptionOptionAdmin)
