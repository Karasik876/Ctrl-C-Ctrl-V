from django.urls import path
from .views import *

urlpatterns = [
    path('create', TestViewSet.as_view({'post': 'create_post'}), name='create_test'),
    path('detail/<int:id>', TestViewSet.as_view({'get': 'test_detail'}), name='test_detail'),
    path('edit/<int:id>', TestViewSet.as_view({'get': 'edit_get', 'patch': 'edit_post'}), name='test_edit'),
    path('my/', TestViewSet.as_view({'get': 'user_tests'}), name='user_tests'),
    path('delete/<int:id>', TestViewSet.as_view({'delete': 'delete_test'}), name='delete_test'),
]
