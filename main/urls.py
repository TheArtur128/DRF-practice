from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from main import views


urlpatterns = format_suffix_patterns([
    path('temporary-message/<int:id>', views.local_message_resource),
    path('temporary-message-list', views.local_message_list_resource),
])
