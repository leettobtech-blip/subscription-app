from django.contrib import admin
from .models import Content


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'is_premium')
	list_editable = ('is_premium',)
	search_fields = ('title',)
