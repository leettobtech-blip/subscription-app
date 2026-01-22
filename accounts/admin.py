from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Device

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ('id', 'email', 'is_active', 'is_staff', 'date_joined')
	search_fields = ('email',)


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'device_id', 'created_at')
	search_fields = ('user__email', 'device_id')
