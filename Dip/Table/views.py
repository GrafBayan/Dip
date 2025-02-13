from django.shortcuts import render, redirect
from .models import Room
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def ches_page(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        if room_name:
            room = Room.objects.create(name=room_name)
            return redirect('chess_page', room_id=room.id)

    rooms = Room.objects.all()

    paginator = Paginator(rooms, 8)
    page_number = request.GET.get('page')
    try:
        rooms = paginator.page(page_number)
    except PageNotAnInteger:
        rooms = paginator.page(1)
    except EmptyPage:
        rooms = paginator.page(paginator.num_pages)

    return render(request, 'Table/ches_page.html', {'rooms': rooms})

def chess_page(request, room_id):
    room = Room.objects.get(id=room_id)
    return render(request, 'Table/chess.html', {'room': room})

def game_page(request):
    return render(request, 'Table/game_page.html')

@csrf_exempt  # Не забыть потом убрать
def start_game(request):
    if request.method == 'POST':
        subprocess.Popen(['python', 'chess_game/ch.py'])
        return JsonResponse({'status': 'Game started!'})
    return JsonResponse({'status': 'Invalid request'}, status=400)

@csrf_exempt  # добавить защиту CSRF позже
def close_room(request, room_id):
    if request.method == 'POST':
        try:
            room = Room.objects.get(id=room_id)
            room.delete()
            return JsonResponse({'status': 'Room closed!'})
        except Room.DoesNotExist:
            return JsonResponse({'status': 'Room not found'}, status=404)
    return JsonResponse({'status': 'Invalid request'}, status=400)