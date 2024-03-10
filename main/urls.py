from django.urls import path

from main import views


urlpatterns = [
    path('', views.local_message_list)
]
