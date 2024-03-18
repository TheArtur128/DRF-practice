from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from main import views


urlpatterns = format_suffix_patterns([
    path('temporary-messages', views.local_message_list_resource),
    path('temporary-message/<int:id>', views.LocalMessageResource.as_view()),
    path('long-term-messages', views.OrmMessageListResource.as_view()),
    path('long-term-message/<int:id>', views.OrmMessageResource.as_view()),
])
