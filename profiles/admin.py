from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'default_phone_number', 'default_street_address1', 'default_town_or_city', 'default_postcode', 'default_country', 'has_active_subscription', 'stripe_customer_id')
    search_fields = ('user__username', 'full_name', 'has_active_subscription' , 'default_country__name')
    list_filter = ('has_active_subscription', 'default_country',)


admin.site.register(UserProfile, UserProfileAdmin)
