from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'default_country',
                    'default_town_or_city', 'has_active_subscription')
    search_fields = ('user__username', 'default_town_or_city',
                     'default_country__name')
    list_filter = ('has_active_subscription', 'default_country',)


admin.site.register(UserProfile, UserProfileAdmin)
