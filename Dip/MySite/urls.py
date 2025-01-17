from django.urls import path
from .views import register, home, login_view, profile_view, accept_invite, decline_invite
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('profile/', profile_view, name='profile'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('invite/accept/<int:invite_id>/', accept_invite, name='accept_invite'),
    path('invite/decline/<int:invite_id>/', decline_invite, name='decline_invite'),
]