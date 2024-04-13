from django.contrib import admin
from .models import SubscriptionOption, UserSubscriptionOption


class SubscriptionOptionAdmin(admin.ModelAdmin):
    list_display = ('category', 'number_of_books', 'subscription_type', 'stripe_price_id')  # noqa

    list_filter = ('category', 'subscription_type')
    search_fields = ('category', 'subscription_type')


class UserSubscriptionOptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription_option', 'calculated_price', 'start_date', 'end_date', 'is_active')

    def display_selected_books(self, obj):
        selected_books = obj.get_selected_books()
        return ', '.join([book.title for book in selected_books])
    display_selected_books.short_description = 'Selected Books'

    list_filter = ('user', 'subscription_option', 'is_active')
    search_fields = ('user', 'subscription_option')


admin.site.register(UserSubscriptionOption, UserSubscriptionOptionAdmin)
admin.site.register(SubscriptionOption, SubscriptionOptionAdmin)
