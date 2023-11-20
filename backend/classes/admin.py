from django.contrib import admin
from .models import *


class ClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'class_name',  'class_number', 'class_letter', 'user', 'created_at')
    list_display_links = ('id', 'class_name')
    search_fields = ('id', 'class_name',  'class_number', 'class_letter')
    list_filter = ('class_number', 'class_letter', 'created_at')
    readonly_fields = ('id', 'user', 'created_at')
    save_on_top = True


admin.site.register(Class, ClassAdmin)
