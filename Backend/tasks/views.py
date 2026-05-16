import json
import uuid
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta


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

    if not request.user.is_authenticated:
        return JsonResponse(
            {
                'success': False,
                'error': 'Authentication required'
            },
            status=401
        )

    try:
        if request.content_type and 'application/json' in request.content_type:
            data = json.loads(request.body)
        else:
            data = request.POST

        # VALIDACIÓN DE SUSCRIPCIÓN
        from shared.subscription import check_user_limit
        limit_response = check_user_limit(request.user, 'tasks')
        if limit_response:
            return limit_response

        name = data.get('name') or data.get('title')

        if not name:
            return JsonResponse(
                {
                    'success': False,
                    'error': 'Name is required'
                },
                status=400
            )

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

        due_date = data.get('due_date') or None
        due_time = data.get('due_time') or None
        priority = data.get('priority', 'medium')
        status = data.get('status', 'pending')

        task = TaskFlow.objects.create(
            user=request.user,
            library=library_content,
            name=name,
            slug=str(uuid.uuid4())[:8],
            description=data.get('description', ''),
            completed=False,
            priority=priority,
            status=status,
            due_date=due_date,
            due_time=due_time,
        )

        serializer = TaskFlowSerializer(task)

        return JsonResponse(
            {
                'success': True,
                'task': serializer.serialize()
            },
            status=201
        )

    except Exception as e:

        return JsonResponse(
            {
                'success': False,
                'error': str(e)
            },
            status=400
        )
    
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
        
        if 'due_date' in data:
            task.due_date = data['due_date']

        if 'due_time' in data:
            task.due_time = data['due_time']

        if 'priority' in data:
            task.priority = data['priority']

        if 'status' in data:
            task.status = data['status']
                
        task.save()
        
        serializer = TaskFlowSerializer(task)
        return JsonResponse({'success': True, 'task': serializer.serialize()}, safe=False)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@csrf_exempt
def delete_task(request, id):
    if request.method not in ['POST', 'DELETE']:
        return HttpResponseNotAllowed(['POST', 'DELETE'])

    if not request.user.is_authenticated:
        return JsonResponse(
            {'success': False, 'error': 'Authentication required'},
            status=401
        )

    try:
        task = get_object_or_404(
            TaskFlow,
            id=id,
            user=request.user
        )

        content = task.library

        task.delete()

        if content:
            content.delete()

        return JsonResponse(
            {
                'success': True,
                'message': 'Task deleted successfully'
            },
            status=200
        )

    except Exception as e:

        return JsonResponse(
            {
                'success': False,
                'error': str(e)
            },
            status=400
        )

@csrf_exempt
def planner(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    month = request.GET.get('month')
    year = request.GET.get('year')

    if not month or not year:
        return JsonResponse(
            {'success': False, 'error': 'month and year are required'},
            status=400
        )

    tasks = TaskFlow.objects.filter(
        user=request.user,
        due_date__month=month,
        due_date__year=year
    )

    serializer = TaskFlowSerializer(tasks)
    return JsonResponse(serializer.serialize(), safe=False)
