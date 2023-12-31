from django.contrib import admin
from .models import *


class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'last_login', 'created_at')
    list_display_links = ('id', 'email')
    search_fields = ('id', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'last_login', 'created_at')
    readonly_fields = ('id', 'email', 'password', 'last_login', 'is_active', 'created_at')
    save_on_top = True


admin.site.register(UserAccount, UserAccountAdmin)

admin.site.site_title = 'Управление Scanner'
admin.site.site_header = 'Управление Scanner'