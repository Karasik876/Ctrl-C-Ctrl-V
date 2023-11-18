from django.urls import path
from .views import *

urlpatterns = [
    path('tests/create', TestViewSet.as_view({'post': 'create_post'}), name='create_test'),
    path('tests/detail/<int:id>', TestViewSet.as_view({'get': 'test_detail'}), name='test_detail')
]
