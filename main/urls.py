from django.urls import path

from main import views


urlpatterns = [
    path('temporary-message/<int:id>', views.local_message),
    path('temporary-message-list', views.local_message_list),
]
