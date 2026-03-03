from shared.decorators import require_http_methods
from django.http import JsonResponse

from .models import TaskFlow
from .serializers import TaskFlowSerializer


@require_http_methods('GET')
def task_list(request):
    tasks = TaskFlow.objects.all()
    serializer = TaskFlowSerializer(tasks)
    return serializer.json_response()

@require_http_methods('GET')
def task_detail(request, task_id):
    try:
        task = TaskFlow.objects.get(id=task_id)
    except TaskFlow.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)

    serializer = TaskFlowSerializer(task)
    return serializer.json_response()

@require_http_methods('POST')
def create_task(request):
    if request.method == 'POST':
        data = request.POST
        serializer = TaskFlowSerializer(data=data)
        if serializer.is_valid():
            task = serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    
@require_http_methods('POST')   
def edit_task(request, task_id):
    try:
        task = TaskFlow.objects.get(id=task_id)
    except TaskFlow.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)

    if request.method == 'PUT':
        data = request.PUT
        serializer = TaskFlowSerializer(task, data=data)
        if serializer.is_valid():
            task = serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    
@require_http_methods('DELETE')
def delete_task(request, task_id):
    try:
        task = TaskFlow.objects.get(id=task_id)
    except TaskFlow.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)

    if request.method == 'DELETE':
        task.delete()
        return JsonResponse({'message': 'Task deleted successfully'}, status=204) 