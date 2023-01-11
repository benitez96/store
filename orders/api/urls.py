from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path


from .views import OrderView

urlpatterns = [
    path('orders/', OrderView.as_view()),
]

# urlpatterns = format_suffix_patterns(urlpatterns)