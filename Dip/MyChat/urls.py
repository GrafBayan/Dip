from django.urls import path
from .views import chat_page, chat_list, create_chat, send_message, send_invite

urlpatterns = [
    path('chat_list/', chat_list, name='chat_list'),
    path('chat/<int:chat_id>/', chat_page, name='chat_page'),
    path('chat/<int:chat_id>/send_message/', send_message, name='send_message'),
    path('cr_chat/', create_chat, name='create_chat'),
    path('chat/<int:chat_id>/invite/', send_invite, name='send_invite'),
]