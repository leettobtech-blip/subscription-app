from django.contrib import admin
from .models import SubscriptionPlan, UserSubscription


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'max_devices', 'price', 'allows_premium')
	list_editable = ('max_devices', 'price', 'allows_premium')
	search_fields = ('name',)


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'plan', 'is_active')
	search_fields = ('user__email', 'plan__name')
