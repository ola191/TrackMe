from django.urls import path
from .views import register_view, login_view, logout_view, friends_view, search_users, send_friend_request, \
    respond_friend_request

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('friends/', friends_view, name='friends'),
    path('friends/search/', search_users, name='search_users'),
    path('friends/send_request/', send_friend_request, name='send_friend_request'),
    path('friends/respond_request/', respond_friend_request, name='respond_friend_request'),
]
