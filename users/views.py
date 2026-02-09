from accounts.views import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EditProfileForm


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
def leave(request):
    user = request.user
    profile = user.profile
    if profile.is_teacher():
        return HttpResponseForbidden('Teachers cannot leave the platform')
    messages.success(request, 'Good bye! Hope to see you soon.')
    logout(request)
    user.delete()
    return redirect('index')
