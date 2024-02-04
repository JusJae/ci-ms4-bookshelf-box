from django.contrib import admin
from .models import SubscriptionOption


class SubscriptionOptionAdmin(admin.ModelAdmin):
    list_display = ('category', 'number_of_books', 'subscription_type', 'display_calculated_price', 'get_random_books')  # noqa

    def display_calculated_price(self, obj):
        return obj.calculate_price()
    display_calculated_price.short_description = 'Calculated Price'

    def display_selected_books(self, obj):
        return obj.random_books()
    display_selected_books.short_description = 'Selected Books'

    list_filter = ('category', 'subscription_type')
    search_fields = ('category', 'subscription_type')


admin.site.register(SubscriptionOption, SubscriptionOptionAdmin)
