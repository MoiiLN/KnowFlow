from django.shortcuts import render

from shared.decorators import require_http_methods
from django.http import JsonResponse

from .models import TimerFlow, StudySession
from .serializers import TimerFlowSerializer, StudySessionSerializer


@require_http_methods('GET')
def timerflow_list(request):
    timers = TimerFlow.objects.all()
    serializer = TimerFlowSerializer(timers)
    return serializer.json_response()


@require_http_methods('POST')
def create_timerflow(request):
    data = request.POST
    serializer = TimerFlowSerializer(data=data)

    if serializer.is_valid():
        timer = serializer.save()
        return JsonResponse(serializer.data, status=201)

    return JsonResponse(serializer.errors, status=400)


@require_http_methods('GET')
def studysession_list(request):
    sessions = StudySession.objects.all()
    serializer = StudySessionSerializer(sessions)
    return serializer.json_response()


@require_http_methods('POST')
def create_studysession(request):
    data = request.POST
    serializer = StudySessionSerializer(data=data)

    if serializer.is_valid():
        session = serializer.save()
        return JsonResponse(serializer.data, status=201)

    return JsonResponse(serializer.errors, status=400)