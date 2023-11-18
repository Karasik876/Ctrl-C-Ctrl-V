from django.contrib import admin
from .models import *


class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'test_name', 'user')
    list_display_links = ('id', 'test_name')
    search_fields = ('id', 'test_name')
    readonly_fields = ('id', 'user', 'questions', 'choices', 'answers')
    save_on_top = True


admin.site.register(Test, TestAdmin)
