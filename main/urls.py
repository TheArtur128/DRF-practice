from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from main import views


app_name = "main"

urlpatterns = format_suffix_patterns([
    path('root', views.root_endpoint, name='root'),
    path(
        'temporary-messages',
        views.local_message_list_endpoint,
        name='temporary-messages',
    ),
    path(
        'temporary-message/<int:id>',
        views.LocalMessageEndpoint.as_view(),
        name='temporary-message',
    ),
    path(
        'long-term-messages',
        views.OrmMessageListEndpoint.as_view(),
        name='long-term-messages',
    ),
    path(
        'long-term-message/<int:id>',
        views.OrmMessageEndpoint.as_view(),
        name='long-term-message',
    ),
    path('users', views.UserListEndpoint.as_view(), name='users'),
    path('user/<int:pk>', views.UserEndpoint.as_view(), name='user'),
])
