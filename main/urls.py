from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

from main import views


app_name = "main"

read_only_user_list_view = views.ReadOnlyUserViewSet.as_view({'get': 'list'})

profile_list_view = views.ProfileViewSet.as_view({'get': 'list'})
profile_view = views.ProfileViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy',
})

router = DefaultRouter()

router.register('read-only-users', views.ReadOnlyUserViewSet, 'read-only-user')
router.register('profiles', views.ProfileViewSet, 'profile')

urlpatterns = format_suffix_patterns([
    path('root', views.root_view, name='root'),
    path(
        'temporary-messages',
        views.local_message_list_view,
        name='temporary-messages',
    ),
    path(
        'temporary-message/<int:id>',
        views.LocalMessageView.as_view(),
        name='temporary-message',
    ),
    path(
        'long-term-messages',
        views.OrmMessageListView.as_view(),
        name='long-term-messages',
    ),
    path(
        'long-term-message/<int:id>',
        views.OrmMessageView.as_view(),
        name='long-term-message',
    ),
    path('users', views.UserListView.as_view(), name='users'),
    path('user/<int:pk>', views.UserView.as_view(), name='user'),
    path('read-only-users', read_only_user_list_view, name='read-only-users'),
    path('profiles', profile_list_view, name='profiles'),
    path('profile/<int:id>', profile_view, name='profile'),
])

urlpatterns.append(path('other/', include(router.urls)))
