from django.urls import path
from .views import *

urlpatterns = [
    path('create', TestViewSet.as_view({'post': 'create_post'}), name='create_test'),
    path('detail/<int:id>', TestViewSet.as_view({'get': 'test_detail'}), name='test_detail'),
    path('', TestListView.as_view(), name='test_list'),
    path('edit/<int:id>', TestViewSet.as_view({'get': 'edit_get', 'patch': 'edit_post'}), name='test_edit'),
    path('delete/<int:id>', TestViewSet.as_view({'delete': 'delete_test'}), name='delete_test'),
]
