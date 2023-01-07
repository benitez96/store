from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


from .views import (
    ProductView,
    ProductDetailView,
    # ImageView,
)

urlpatterns = [
    path('products/', ProductView.as_view()),
    path('products/<str:slug>', ProductDetailView.as_view()),
    # path('images/<int:pk>', ImageView.as_view(), name='image-detail'),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
