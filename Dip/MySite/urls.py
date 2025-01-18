from django.urls import path
from .views import register, home, login_view, profile_view, accept_invite, decline_invite, accept_join_request, decline_join_request
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('profile/', profile_view, name='profile'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('invite/accept/<int:invite_id>/', accept_invite, name='accept_invite'),
    path('invite/decline/<int:invite_id>/', decline_invite, name='decline_invite'),
    path('accept-join-request/<int:request_id>/', accept_join_request, name='accept_join_request'),
    path('decline-join-request/<int:request_id>/', decline_join_request, name='decline_join_request'),
]