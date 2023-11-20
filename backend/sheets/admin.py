from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *


class SheetAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_name_photo',  'test', 'user', 'the_class', 'scanned_date')
    list_display_links = ('id', 'get_name_photo')
    search_fields = ('id',)
    list_filter = ('scanned_date',)
    fields = ('id', 'get_name_photo',  'test', 'user', 'the_class', 'get_sheet_photo', 'student_answers', 'result', 'scanned_date')
    readonly_fields = ('id', 'get_name_photo',  'test', 'user', 'the_class', 'get_sheet_photo', 'student_answers', 'result', 'scanned_date')
    save_on_top = True

    def get_name_photo(self, object):
        return mark_safe(f'<img src="{object.name_image}" width=200>') if object.name_image else '-'

    def get_sheet_photo(self, object):
        return mark_safe(f'<img src="{object.sheet_image}" width=500>') if object.sheet_image else '-'

    get_name_photo.short_description = 'Имя'
    get_sheet_photo.short_description = 'Бланк'


admin.site.register(Sheet, SheetAdmin)
