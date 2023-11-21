from django.urls import path
from .views import *

urlpatterns = [
    path('create', ClassViewSet.as_view({'post': 'create_post'}), name='create_class'),
    path('detail/<int:id>', ClassViewSet.as_view({'get': 'class_detail'}), name='class_detail'),
    path('edit/<int:id>', ClassViewSet.as_view({'get': 'edit_get', 'patch': 'edit_post'}), name='class_edit'),
    path('delete/<int:id>', ClassViewSet.as_view({'delete': 'delete_class'}), name='delete_class'),
]
