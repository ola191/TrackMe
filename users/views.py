import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from django.views.decorators.csrf import csrf_exempt

from users.forms import CustomUserCreationForm
from users.models import Friendship, CustomUser


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {"form": form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {"form": form})

@login_required
def friends_view(request):
    user = request.user

    friends = Friendship.objects.filter(
        (Q(from_user=user) | Q(to_user=user)),
        status='accepted'
    )

    blocked_users = Friendship.objects.filter(
        (Q(from_user=user) | Q(to_user=user)),
        status__in=['blocked', 'declined']
    )

    incoming_requests = Friendship.objects.filter(
        to_user=user, status='requested'
    )

    return render(request, 'users/friends.html', {
        'friends': friends,
        'blocked_users': blocked_users,
        'incoming_requests': incoming_requests
    })

@login_required
def search_users(request):
    query = request.GET.get('search_query', '')
    users = CustomUser.objects.filter(username__icontains=query).exclude(id=request.user.id)
    data = {
        'users': [{'id': user.id, 'username': user.username} for user in users]
    }
    return JsonResponse(data)

@csrf_exempt
@login_required
def send_friend_request(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        to_user = get_object_or_404(CustomUser, id=data.get('user_id'))
        from_user = request.user

        if Friendship.objects.filter(from_user=from_user, to_user=to_user).exists():
            return JsonResponse({'message': 'Request already sent', 'success': False})

        Friendship.objects.create(from_user=from_user, to_user=to_user, status='requested')
        return JsonResponse({'message': 'Friend request sent', 'success': True})

@csrf_exempt
@login_required
def respond_friend_request(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        friendship = get_object_or_404(Friendship, id=data.get('request_id'), to_user=request.user)
        action = data.get('action')

        if action == 'accept':
            friendship.status = 'accepted'
        elif action == 'decline':
            friendship.status = 'declined'
        elif action == 'block':
            friendship.status = 'blocked'
        friendship.save()

        return JsonResponse({'message': f'Request {action}ed', 'success': True})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
