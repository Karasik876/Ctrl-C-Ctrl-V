from django.urls import path
from .views import *

urlpatterns = [
    path('create', TestViewSet.as_view({'post': 'create_post'}), name='create_test'),
    path('detail/<int:id>', TestViewSet.as_view({'get': 'test_detail'}), name='test_detail')
]
