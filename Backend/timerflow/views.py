import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from shared.decorators import require_http_methods

from .models import TimerFlow, StudySession
from .serializers import TimerFlowSerializer, StudySessionSerializer

@require_http_methods('GET')
def timerflow_settings(request):
    settings, created = TimerFlow.objects.get_or_create(user=request.user)
    serializer = TimerFlowSerializer(settings)
    return JsonResponse(serializer.serialize(), safe=False)


@csrf_exempt
@require_http_methods('POST')
def update_timerflow_settings(request):
    settings, created = TimerFlow.objects.get_or_create(user=request.user)
    try:
        data = json.loads(request.body)
        if 'default_minutes' in data: settings.default_minutes = data['default_minutes']
        if 'short_break' in data: settings.short_break = data['short_break']
        if 'long_break' in data: settings.long_break = data['long_break']
        if 'cycle_before_long_break' in data: settings.cycle_before_long_break = data['cycle_before_long_break']
        
        settings.save()
        serializer = TimerFlowSerializer(settings)
        return JsonResponse({'success': True, 'settings': serializer.serialize()})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_http_methods('GET')
def studysession_list(request):
    sessions = StudySession.objects.filter(user=request.user).order_by('-started_at')[:10]
    serializer = StudySessionSerializer(sessions)
    return JsonResponse(serializer.serialize(), safe=False)


@csrf_exempt
@require_http_methods('POST')
def create_studysession(request):
    try:
        data = json.loads(request.body)
        session = StudySession.objects.create(
            user=request.user,
            planned_minutes=data.get('planned_minutes', 25),
            session_type=data.get('session_type', 'work'),
            completed=data.get('completed', False),
            ended_at=timezone.now() if data.get('completed') else None
        )
        serializer = StudySessionSerializer(session)
        return JsonResponse({'success': True, 'session': serializer.serialize()}, status=201)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)