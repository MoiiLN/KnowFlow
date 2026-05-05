import json
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta

from accounts.views import logout as django_logout
from shared.decorators import require_http_methods

from .forms import EditProfileForm
from .models import Profile
from library.models import Library
from flashcards.models import FlowCard
from notes.models import Note
from tasks.models import TaskFlow
from knowtionaries.models import Knowtionary

@csrf_exempt
@require_http_methods('POST')
def auth(request):
    try:
        payload = json.loads(request.body)
        username = payload.get('username')
        password = payload.get('password')

        if user := authenticate(username=username, password=password):
            try:
                return JsonResponse({'token': user.token.key})
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Token not found'}, status=404)
        return JsonResponse({'error': 'Invalid credentials'}, status=401)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user)
    context = {'user': user, 'profile': profile, 'role': profile.role}
    return render(request, 'users/detail.html', context)


@login_required
def edit_profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    avatar = profile.avatar
    if request.method == 'POST':
        if (form := EditProfileForm(request.POST, request.FILES, instance=profile)).is_valid():
            form.save()
            messages.success(request, 'User profile has been successfully saved.')
            return redirect('user-detail', username=user.username)
    else:
        form = EditProfileForm(instance=profile)
    return render(request, 'users/edit.html', {'form': form, 'avatar': avatar})


def me_api_unauthorized(request):
    """Devuelve JSON con info del usuario actual, incluyendo TODAS las estadísticas reales"""
    if request.user.is_authenticated:
        user = request.user
        profile, created = Profile.objects.get_or_create(user=user)
        
        # Streak Logic
        today = timezone.now().date()
        last_active = profile.last_active_date
        if hasattr(last_active, 'date'):
            last_active = last_active.date()
            
        if last_active < today:
            if profile.last_active_date == today - timedelta(days=1):
                profile.streak += 1
            else:
                profile.streak = 1
            profile.last_active_date = today
            profile.save()

        # ALL Real Stats with correct filters
        library_count = Library.objects.filter(user=user).count()
        flashcard_count = FlowCard.objects.filter(user=user).count()
        note_count = Note.objects.filter(content__user=user).count()
        task_count = TaskFlow.objects.filter(user=user).count()
        knowtionary_count = Knowtionary.objects.filter(content__user=user).count()
        
        return JsonResponse({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'date_joined': user.date_joined.isoformat(),
            'bio': profile.bio,
            'avatar': profile.avatar.url if profile.avatar else None,
            'role': profile.role,
            'stats': {
                'libraries': library_count,
                'flashcards': flashcard_count,
                'notes': note_count,
                'tasks': task_count,
                'knowtionaries': knowtionary_count,
                'streak': profile.streak
            }
        })
    return JsonResponse({'error': 'Authentication required'}, status=401)

@csrf_exempt
@require_http_methods('POST')
def api_edit_profile(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
        
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
        
    try:
        new_email = request.POST.get('email')
        if new_email:
            user.email = new_email
            user.save()
        
        if 'bio' in request.POST:
            profile.bio = request.POST.get('bio')
            
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
            
        profile.save()
        
        return JsonResponse({
            'success': True,
            'user': {
                'username': user.username,
                'email': user.email,
                'bio': profile.bio,
                'avatar': profile.avatar.url if profile.avatar else None,
                'role': profile.role
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods('POST')
def api_delete_account(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    user = request.user
    django_logout(request)
    user.delete()
    return JsonResponse({'success': True})


@login_required
def leave(request):
    user = request.user
    django_logout(request)
    user.delete()
    messages.success(request, 'Good bye! Hope to see you soon.')
    return redirect('index')
