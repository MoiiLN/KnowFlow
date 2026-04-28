import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from shared.decorators import require_http_methods

from .models import Knowtionary, Question
from .serializers import KnowtionarySerializer
from library.models import LibraryContent

@require_http_methods('GET')
def knowtionary_list(request):
    # Filter by user via the content relationship
    quizzes = Knowtionary.objects.filter(content__user=request.user)
    serializer = KnowtionarySerializer(quizzes)
    return JsonResponse(serializer.serialize(), safe=False)


@require_http_methods('GET')
def knowtionary_detail(request, quiz_id):
    quiz = get_object_or_404(Knowtionary, id=quiz_id, content__user=request.user)
    serializer = KnowtionarySerializer(quiz)
    return JsonResponse(serializer.serialize(), safe=False)


@csrf_exempt
@require_http_methods('POST')
def add_knowtionary(request):
    try:
        data = json.loads(request.body)
            
        library_content_id = data.get('library_content_id')
        if not library_content_id:
            return JsonResponse({'success': False, 'error': 'Library content ID is required'}, status=400)
            
        library_content = get_object_or_404(LibraryContent, id=library_content_id, user=request.user)
        
        quiz = Knowtionary.objects.create(
            content=library_content,
            description=data.get('description', '')
        )
        
        serializer = KnowtionarySerializer(quiz)
        return JsonResponse({'success': True, 'quiz': serializer.serialize()}, status=201)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods('PUT', 'PATCH')
def edit_knowtionary(request, quiz_id=None):
    try:
        data = json.loads(request.body)
        target_id = quiz_id or data.get('id')
        
        knowtionary = get_object_or_404(Knowtionary, id=target_id, content__user=request.user)

        if 'description' in data:
            knowtionary.description = data['description']
            knowtionary.save()
            
        serializer = KnowtionarySerializer(knowtionary)
        return JsonResponse({'success': True, 'quiz': serializer.serialize()}, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def play_knowtionary(request, quiz_id):
    return JsonResponse({'message': 'Play mode not implemented yet'})


def knowtionary_score(request, quiz_id):
    return JsonResponse({'message': 'Score logic not implemented yet'})