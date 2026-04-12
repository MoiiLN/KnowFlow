from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import LoginForm, SignupForm


def user_login(request):
    FALLBACK_REDIRECT = '/dashboard'

    if request.user.is_authenticated:
        return redirect(FALLBACK_REDIRECT)
    if request.method == 'POST':
        if (form := LoginForm(request.POST)).is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if user := authenticate(request, username=username, password=password):
                login(request, user)
                return redirect(request.GET.get('next', FALLBACK_REDIRECT))
            else:
                form.add_error(None, 'Incorrect username or password')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def user_signup(request):
    FALLBACK_REDIRECT = '/dashboard'

    if request.user.is_authenticated:
        return redirect(FALLBACK_REDIRECT)
    if request.method == 'POST':
        if (form := SignupForm(request.POST)).is_valid():
            user = form.save()
            messages.success(request, 'Welcome to Lumino. Nice to see you!')
            login(request, user)
            return redirect(FALLBACK_REDIRECT)
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})


def user_logout(request):
    FALLBACK_REDIRECT = '/dashboard'
    logout(request)
    return redirect(FALLBACK_REDIRECT)

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
@require_http_methods(["POST"])
def api_login(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({'success': true, 'user': {'username': user.username}})
        else:
            return JsonResponse({'error': 'Credenciales inválidas'}, status=400)
    except:
        return JsonResponse({'error': 'Error en login'}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def api_signup(request):
    try:
        data = json.loads(request.body)
        form = SignupForm(data)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({'success': true, 'user': {'username': user.username}})
        return JsonResponse({'error': form.errors}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def api_logout(request):
    logout(request)
    return JsonResponse({'success': true})
