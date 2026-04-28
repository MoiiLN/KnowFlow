import json
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from shared.decorators import require_http_methods

from .models import TaskFlow
from .serializers import TaskFlowSerializer

@require_http_methods('GET')
def task_list(request):
    # Filter by user
    tasks = TaskFlow.objects.filter(user=request.user)
    serializer = TaskFlowSerializer(tasks)
    return JsonResponse(serializer.serialize(), safe=False)

@require_http_methods('GET')
def task_detail(request, task_id):
    task = get_object_or_404(TaskFlow, id=task_id, user=request.user)
    serializer = TaskFlowSerializer(task)
    return JsonResponse(serializer.serialize(), safe=False)

@csrf_exempt
@require_http_methods('POST')
def create_task(request):
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST
            
        title = data.get('title')
        if not title:
            return JsonResponse({'success': False, 'error': 'Title is required'}, status=400)
            
        task = TaskFlow.objects.create(
            user=request.user,
            title=title,
            description=data.get('description', ''),
            status=data.get('status', 'P'),
            priority=data.get('priority', 'M'),
            due_date=data.get('due_date')
        )
        
        serializer = TaskFlowSerializer(task)
        return JsonResponse({'success': True, 'task': serializer.serialize()}, status=201)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods('PUT', 'PATCH', 'POST')
def edit_task(request, task_id):
    task = get_object_or_404(TaskFlow, id=task_id, user=request.user)
    
    try:
        data = json.loads(request.body)
        
        for field in ['title', 'description', 'status', 'priority', 'due_date']:
            if field in data:
                setattr(task, field, data[field])
                
        task.save()
        
        serializer = TaskFlowSerializer(task)
        return JsonResponse({'success': True, 'task': serializer.serialize()}, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods('DELETE', 'POST')
def delete_task(request, task_id):
    task = get_object_or_404(TaskFlow, id=task_id, user=request.user)
    task.delete()
    return JsonResponse({'message': 'Task deleted successfully'}, status=204)