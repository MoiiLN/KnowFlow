import json

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from accounts.views import logout
from shared.decorators import require_http_methods

from .forms import EditProfileForm
from .models import Profile


@csrf_exempt
@require_http_methods('POST')
def auth(request):
    payload = json.loads(request.body)

    username = payload['username']

    password = payload['password']

    if user := authenticate(username=username, password=password):
        try:
            return JsonResponse({'token': user.token.key})

        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Token not found'}, status=404)

    return JsonResponse({'error': 'Invalid credentials'}, status=401)


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    role = profile.role
    context = {'user': user, 'profile': profile, 'role': role}
    return render(request, 'users/detail.html', context)


@login_required
def edit_profile(request):
    user = request.user
    profile = user.profile
    avatar = profile.avatar
    if request.method == 'POST':
        if (form := EditProfileForm(request.POST, request.FILES, instance=profile)).is_valid():
            form.save()
            messages.success(request, 'User profile has been successfully saved.')
            return redirect('user-detail', username=user.username)
    else:
        form = EditProfileForm(instance=profile)
    return render(request, 'users/edit.html', {'form': form, 'avatar': avatar})


@login_required
def me_api(request):
    user = request.user
    return JsonResponse({
        'id': user.id,
        'username': user.username,
        'email': user.email,
    })


@login_required
def leave(request):
    user = request.user
    profile = user.profile
    if not Profile.is_member():
        messages.info('Are you sure?')
    messages.success(request, 'Good bye! Hope to see you soon.')
    logout(request)
    user.delete()
    return redirect('index')
