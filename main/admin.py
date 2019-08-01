from django.contrib import admin

from .models import PressRu, PressEn, Email


@admin.register(PressRu)
class PressRuAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'source', 'added_at', 'id')
	list_filter  = ('added_at',)


@admin.register(PressEn)
class PressEnAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'source', 'added_at', 'id')
	list_filter  = ('added_at',)


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
	list_display = ('sender_name', 'reply_email', 'creation_date', 'sender_ip', 'id')
	list_filter  = ('creation_date',)