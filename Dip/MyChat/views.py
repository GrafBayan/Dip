from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Chat, Message, User, ChatInvite, ChatJoinRequest
from django.contrib import messages as django_messages
import json
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def chat_list(request):
    all_chats = Chat.objects.all()
    user = request.user
    user_chats = Chat.objects.filter(Q(users=user) | Q(creator=user)).distinct()
    search_query = request.GET.get('search', '')

    if search_query:
        all_chats = all_chats.filter(name__icontains=search_query)

    # Пагинация
    paginator = Paginator(all_chats, 8)
    page_number = request.GET.get('page')
    try:
        chats = paginator.page(page_number)
    except PageNotAnInteger:
        chats = paginator.page(1)
    except EmptyPage:
        chats = paginator.page(paginator.num_pages)

    return render(request, 'MyChat/chat_home.html', {
        'chats': chats,
        'user_chats': user_chats,
        'search_query': search_query
    })


@login_required
def chat_page(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    # Проверяем, состоит ли пользователь в чате или является его создателем
    if not (chat.users.filter(id=request.user.id).exists() or chat.creator == request.user):
        existing_request = ChatJoinRequest.objects.filter(chat=chat, user=request.user).first()

        if existing_request:
            if existing_request.status == 'declined':
                existing_request.delete()
                ChatJoinRequest.objects.create(chat=chat, user=request.user)
                django_messages.success(request, 'Ваш запрос на вступление в чат отправлен создателю.')
            else:
                django_messages.warning(request, 'Вы уже отправили запрос на вступление в этот чат.')
        else:
            # Если запроса нет, создаем новый
            ChatJoinRequest.objects.create(chat=chat, user=request.user)
            django_messages.success(request, 'Ваш запрос на вступление в чат отправлен создателю.')

        return redirect('chat_list')

    chat_messages = chat.messages.all()
    existing_users = chat.users.all()
    available_users = User.objects.exclude(id__in=existing_users.values_list('id', flat=True))
    user_chats = Chat.objects.filter(Q(users=request.user) | Q(creator=request.user)).distinct()
    context = {
        'chat': chat,
        'messages': chat_messages,
        'available_users': available_users,
        'user_chats': user_chats,
    }
    return render(request, 'MyChat/chat.html', context)

@csrf_exempt
@login_required
def send_message(request, chat_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data.get('text')
        user = request.user
        chat = get_object_or_404(Chat, id=chat_id)
        message = Message.objects.create(chat=chat, user=user, text=text)
        return JsonResponse({
            'username': user.username,
            'text': message.text
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def create_chat(request):
    if request.method == 'POST':
        chat_name = request.POST.get('chat_name')
        invited_users_ids = request.POST.getlist('invited_users')

        if Chat.objects.filter(name=chat_name).exists():
            django_messages.error(request, "Чат с таким названием уже существует.")
            return render(request, 'MyChat/create_chat.html', {'users': User.objects.all()})

        new_chat = Chat.objects.create(name=chat_name, creator=request.user)
        new_chat.users.add(request.user)

        for user_id in invited_users_ids:
            try:
                user = User.objects.get(id=user_id)
                new_chat.invited_users.add(user)

                # Создаем приглашение с указанием отправителя
                ChatInvite.objects.create(chat=new_chat, user=user, inviter=request.user)

            except User.DoesNotExist:
                django_messages.error(request, f"Пользователь с ID {user_id} не найден.")

        return redirect('chat_page', chat_id=new_chat.id)

    users = User.objects.exclude(id=request.user.id)
    return render(request, 'MyChat/create_chat.html', {'users': users})


@login_required
def send_invite(request, chat_id):
    if request.method == 'POST':
        chat = get_object_or_404(Chat, id=chat_id)
        data = json.loads(request.body)
        user_id = data.get('user_id')

        # Проверяем, был ли выбран пользователь
        if not user_id:
            return JsonResponse({'message': 'Пользователь не выбран.'}, status=400)

        existing_invite = ChatInvite.objects.filter(chat=chat, user_id=user_id).first()
        if existing_invite:
            return JsonResponse({'message': 'Пользователь уже приглашен в этот чат.'}, status=400)

        # Создаем новое приглашение с указанием отправителя
        new_invite = ChatInvite.objects.create(chat=chat, user_id=user_id, inviter=request.user)
        return JsonResponse({'message': 'Приглашение отправлено!'})

    return JsonResponse({'message': 'Неверный метод запроса.'}, status=405)

@login_required
def add_user_to_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if chat.creator != request.user:
        return JsonResponse({'message': 'Вы не имеете прав на добавление пользователей.'}, status=403)
    existing_users = chat.users.all()
    available_users = User.objects.exclude(id__in=existing_users.values_list('id', flat=True))

    return render(request, 'your_template.html', {
        'chat': chat,
        'available_users': available_users,
    })


@login_required
def leave_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.user not in chat.users.all():
        return JsonResponse({'message': 'Вы не являетесь участником этого чата.'}, status=403)
    if chat.creator == request.user:
        chat.delete()
        django_messages.success(request, 'Чат был успешно удалён, так как вы были его создателем.')
    else:
        chat.users.remove(request.user)
        django_messages.success(request, 'Вы вышли из чата.')
    return redirect('chat_list')