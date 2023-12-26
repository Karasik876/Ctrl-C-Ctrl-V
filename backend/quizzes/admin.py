from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *


class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'test_name', 'user', 'the_class', 'created_at')
    list_display_links = ('id', 'test_name')
    search_fields = ('id', 'test_name')
    fields = ('id', 'test_name', 'questions', 'choices', 'answers', 'get_sheet_photo', 'template_img', 'user', 'the_class', 'created_at')
    readonly_fields = ('id', 'user', 'the_class',  'questions', 'choices', 'answers', 'created_at', 'get_sheet_photo', 'template_img')
    save_on_top = True

    def get_sheet_photo(self, object):
        print(object)
        return mark_safe(f'<img src="{object.template_img}" width=300>') if object.template_img else '-'

    get_sheet_photo.short_description = 'Шаблон'


admin.site.register(Test, TestAdmin)
