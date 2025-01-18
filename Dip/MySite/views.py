from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from MyChat.models import Chat, ChatInvite, ChatJoinRequest
from django.contrib import messages as django_messages
from django.db.models import Q
from itertools import chain


def home(request):
    if request.method == "POST":
        action = 'chat' if 'chat' in request.POST else 'game' if 'game' in request.POST else None
        if action:
            if request.user.is_authenticated:
                return redirect(f'{action}_list')
            else:
                django_messages.info(request, 'Вы не зарегистрированы. Пожалуйста, зарегистрируйтесь или войдите в систему.')
                return redirect('home')
    return render(request, 'MySite/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
        else:
            print("Form errors:", form.errors)
    else:
        form = UserRegisterForm()
    return render(request, 'MySite/register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Неправильное имя пользователя или пароль.')
    else:
        form = AuthenticationForm()
    return render(request, 'MySite/login.html', {'form': form})


def profile_view(request):
    user = request.user
    chats = Chat.objects.filter(Q(users=user) | Q(creator=user)).distinct()
    invitations = ChatInvite.objects.filter(user=user, status='pending')
    join_requests = ChatJoinRequest.objects.filter(chat__creator=user, status='pending')
    notifications = list(chain(invitations, join_requests))

    return render(request, 'MySite/profile.html', {
        'chats': chats,
        'notifications': notifications,
    })

@login_required
def accept_invite(request, invite_id):
    invite = get_object_or_404(ChatInvite, id=invite_id)
    if invite.user != request.user:
        return JsonResponse({'message': 'Вы не имеете прав на принятие этого приглашения.'}, status=403)
    if invite.chat.users.filter(id=request.user.id).exists():
        return JsonResponse({'message': 'Вы уже являетесь участником этого чата.'}, status=400)

    # Добавляем пользователя в чат и обновляем статус приглашения
    invite.chat.users.add(invite.user)
    invite.status = 'accepted'
    invite.save()
    return JsonResponse({'message': f'Приглашение принято! Вы добавлены в чат "{invite.chat.name}".'})

@login_required
def decline_invite(request, invite_id):
    invite = get_object_or_404(ChatInvite, id=invite_id)
    if invite.user != request.user:
        return JsonResponse({'message': 'Вы не имеете прав на отклонение этого приглашения.'}, status=403)
    invite.status = 'declined'
    invite.save()
    return JsonResponse({'message': 'Приглашение отклонено.'})


@login_required
def accept_join_request(request, request_id):
    join_request = get_object_or_404(ChatJoinRequest, id=request_id)

    # Проверяем, что текущий пользователь является создателем чата
    if join_request.chat.creator != request.user:
        return JsonResponse({'message': 'Вы не имеете прав на принятие этого запроса.'}, status=403)

    # Проверяем, если пользователь уже является участником чата
    if join_request.user in join_request.chat.users.all():
        return JsonResponse({'message': 'Этот пользователь уже является участником чата.'}, status=400)

    # Добавляем пользователя в чат и обновляем статус запроса
    join_request.chat.users.add(join_request.user)
    join_request.status = 'accepted'
    join_request.save()

    return JsonResponse({'message': f'Запрос на вступление принят! {join_request.user.username} добавлен в чат "{join_request.chat.name}".'})



@login_required
def decline_join_request(request, request_id):
    join_request = get_object_or_404(ChatJoinRequest, id=request_id)
    if join_request.chat.creator != request.user:
        return JsonResponse({'message': 'Вы не имеете прав на отклонение этого запроса.'}, status=403)
    join_request.status = 'declined'
    join_request.save()

    return JsonResponse({'message': 'Запрос на вступление отклонён.'})