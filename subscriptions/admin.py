from django.contrib import admin
from .models import SubscriptionPlan, UserSubscriptionOption


# class SubscriptionOptionAdmin(admin.ModelAdmin):
#     list_display = ('category', 'number_of_books', 'subscription_type',)  # noqa

#     def display_selected_books(self, obj):
#         selected_books = obj.get_selected_books()
#         return ', '.join([book.title for book in selected_books])
#     display_selected_books.short_description = 'Selected Books'

#     list_filter = ('category', 'subscription_type')
#     search_fields = ('category', 'subscription_type')

class SubscriptionPlanAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('name', 'number_of_books', 'price')
    list_filter = ('name',)  # Fields to filter by in the sidebar
    # Fields to search in the admin
    search_fields = ('name', 'number_of_books')

    # This method ensures that the price is set when a SubscriptionPlan is saved via the Django Admin
    def save_model(self, request, obj, form, change):
        if not obj.price:
            obj.set_price()
        super().save_model(request, obj, form, change)


class UserSubscriptionOptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'price', 'start_date', 'end_date', 'is_active')

    list_filter = ('user', 'plan', 'is_active')
    search_fields = ('user', 'plan', 'is_active')


admin.site.register(UserSubscriptionOption, UserSubscriptionOptionAdmin)
admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)
