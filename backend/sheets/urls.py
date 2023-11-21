from django.urls import path
from .views import *

urlpatterns = [
    path('create', SheetViewSet.as_view({'post': 'create_post'}), name='create_sheet'),
    path('detail/<int:id>', SheetViewSet.as_view({'get': 'sheet_detail'}), name='sheet_detail'),
    path('delete/<int:id>', SheetViewSet.as_view({'delete': 'delete_sheet'}), name='delete_sheet'),
]
