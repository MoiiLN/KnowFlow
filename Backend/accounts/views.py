from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
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
    # Si ya hay sesión activa, cerrarla primero para evitar falsos positivos
    if request.user.is_authenticated:
        logout(request)
    
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            
            from django.conf import settings
            from users.models import Profile
            profile, _ = Profile.objects.get_or_create(user=user)
            avatar_url = f"https://ui-avatars.com/api/?name={user.username}&background=random&color=fff"
            if profile.avatar:
                try:
                    avatar_url = profile.avatar.url
                except:
                    pass

            return JsonResponse({
                'success': True,
                'user': {
                    'username': user.username,
                    'avatar': avatar_url
                }
            })
        else:
            # Asegurar que no quede sesión parcial
            request.session.flush()
            return JsonResponse({'error': 'Credenciales inválidas'}, status=401)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def api_signup(request):
    try:
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')

        if not all([username, email, password]):
            return JsonResponse({'error': 'Todos los campos son obligatorios'}, status=400)

        User = get_user_model()

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'El usuario ya existe'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'El email ya está registrado'}, status=400)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        # Enviar correo de bienvenida (asíncrono) - Opcional para evitar errores de Redis
        try:
            from .tasks import send_welcome_email_task
            send_welcome_email_task.delay(user.username, user.email)
        except Exception:
            pass
        
        login(request, user)
        
        from users.models import Profile
        profile, _ = Profile.objects.get_or_create(user=user)
        avatar_url = f"https://ui-avatars.com/api/?name={user.username}&background=random&color=fff"
        if profile.avatar:
            try:
                avatar_url = profile.avatar.url
            except:
                pass

        return JsonResponse({
            'success': True, 
            'user': {
                'username': user.username,
                'avatar': avatar_url
            }
        })
    except Exception as e:
        return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def api_logout(request):
    logout(request)
    return JsonResponse({'success': True})
