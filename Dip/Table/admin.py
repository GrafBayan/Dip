from django.contrib import admin
from .models import Room

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_open')  # Отображаем имя и состояние комнаты
    list_filter = ('is_open',)