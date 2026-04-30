import json
import uuid
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

from .models import TaskFlow
from .serializers import TaskFlowSerializer
from library.models import Library, LibraryContent

@csrf_exempt
def task_list(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    tasks = TaskFlow.objects.filter(user=request.user)
    serializer = TaskFlowSerializer(tasks)
    return JsonResponse(serializer.serialize(), safe=False)

@csrf_exempt
def task_detail(request, id):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    task = get_object_or_404(TaskFlow, id=id, user=request.user)
    serializer = TaskFlowSerializer(task)
    return JsonResponse(serializer.serialize(), safe=False)

@csrf_exempt
def create_task(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
        
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST
            
        name = data.get('name') or data.get('title')
        if not name:
            return JsonResponse({'success': False, 'error': 'Name is required'}, status=400)
            
        # Create LibraryContent for the task
        library = Library.objects.filter(user=request.user).first()
        if not library:
            unique_suffix = str(uuid.uuid4())[:8]
            library = Library.objects.create(
                user=request.user,
                name=f"Tasks Library ({request.user.username})",
                slug=f"tasks-{request.user.username}-{unique_suffix}",
            )
            
        library_content = LibraryContent.objects.create(
            user=request.user,
            library=library,
            title=name,
            slug=str(uuid.uuid4())[:8]
        )
        
        task = TaskFlow.objects.create(
            user=request.user,
            library=library_content,
            name=name,
            slug=str(uuid.uuid4())[:8],
            description=data.get('description', ''),
            completed=False
        )
        
        serializer = TaskFlowSerializer(task)
        return JsonResponse({'success': True, 'task': serializer.serialize()}, status=201)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@csrf_exempt
def edit_task(request, id):
    if request.method not in ['POST', 'PUT', 'PATCH']:
        return HttpResponseNotAllowed(['POST', 'PUT', 'PATCH'])
        
    task = get_object_or_404(TaskFlow, id=id, user=request.user)
    
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST
        
        if 'name' in data or 'title' in data:
            task.name = data.get('name') or data.get('title')
            task.library.title = task.name
            task.library.save()
            
        if 'description' in data:
            task.description = data['description']
            
        if 'completed' in data:
            task.completed = data['completed']
                
        task.save()
        
        serializer = TaskFlowSerializer(task)
        return JsonResponse({'success': True, 'task': serializer.serialize()}, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def delete_task(request, id):
    if request.method not in ['POST', 'DELETE']:
        return HttpResponseNotAllowed(['POST', 'DELETE'])
    task = get_object_or_404(TaskFlow, id=id, user=request.user)
    # Also delete the associated library content
    content = task.library
    task.delete()
    content.delete()
    return JsonResponse({'message': 'Task deleted successfully'}, status=204)