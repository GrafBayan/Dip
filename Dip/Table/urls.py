from django.urls import path
from .views import game_page, ches_page, chess_page, start_game, close_room

urlpatterns = [
    path('ches/', ches_page, name='ches_page'),
    path('game/', game_page, name='game_page'),
    path('chess/<int:room_id>/', chess_page, name='chess_page'),
    path('start_game/', start_game, name='start_game'),
    path('close_room/<int:room_id>/', close_room, name='close_room'),
]