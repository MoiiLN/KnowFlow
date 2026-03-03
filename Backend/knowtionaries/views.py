from django.shortcuts import render
from .models import Knowtionary, Question
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from shared.decorators import require_http_methods




@csrf_exempt
@login_required
@require_http_methods('GET')
def knowtionary_list(request):
    pass


def knowtionary_detail(request):
    pass


def add_knowtionary(request):
    pass


def edit_knowtionary(request):
    pass


def play_knowtionary(request):
    pass


def knowtionary_score(request):
    pass
