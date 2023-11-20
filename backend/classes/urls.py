from django.urls import path
from .views import *

urlpatterns = [
    path('create', ClassViewSet.as_view({'post': 'create_post'}), name='create_class'),
    path('detail/<int:id>', ClassViewSet.as_view({'get': 'class_detail'}), name='class_detail')
]
