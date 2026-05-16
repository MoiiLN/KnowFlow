import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from shared.decorators import require_http_methods

from .models import Knowtionary, Question
from .serializers import KnowtionarySerializer
from library.models import LibraryContent

@require_http_methods('GET')
def knowtionary_list(request):
    quizzes = Knowtionary.objects.filter(content__user=request.user)
    serializer = KnowtionarySerializer(quizzes)
    return JsonResponse(serializer.serialize(), safe=False)


@require_http_methods('GET')
def knowtionary_detail(request, slug):
    quiz = get_object_or_404(Knowtionary, content__slug=slug, content__user=request.user)
    serializer = KnowtionarySerializer(quiz)
    return JsonResponse(serializer.serialize(), safe=False)


@csrf_exempt
def add_knowtionary(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    if request.content_type == 'application/json':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest('Invalid JSON')
    else:
        data = request.POST
        
    from shared.subscription import check_user_limit
    limit_response = check_user_limit(request.user, 'knowtionaries')
    if limit_response:
        return limit_response

    content_id = data.get('library_content_id')
    library_content = None

    if content_id and content_id != '1':
        library_content = LibraryContent.objects.filter(
            id=content_id,
            user=request.user
        ).first()

    if not library_content:
        from library.models import Library
        library_id = data.get('library_id')
        
        if library_id:
            library = Library.objects.filter(id=library_id, user=request.user).first()
            if not library:
                pass
        else:
            library = Library.objects.filter(user=request.user).first()

        if not library:
            import uuid
            unique_suffix = str(uuid.uuid4())[:8]

            library = Library.objects.create(
                user=request.user,
                name=f"General ({request.user.username})",
                slug=f"general-{request.user.username}-{unique_suffix}",
                description="Librería automática"
            )

        import uuid
        title = data.get('name') or data.get('title', 'Nuevo Knowtionary')

        try:
            library_content = LibraryContent.objects.create(
                user=request.user,
                library=library,
                title=title,
                slug=data.get('slug') or f"quiz-{str(uuid.uuid4())[:8]}"
            )
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                return JsonResponse({'success': False, 'error': 'Ya existe un knowtionary con ese título en esta librería.'}, status=400)
            raise e

    try:
        max_score = int(data.get('max_score_per_question', 1))
    except ValueError:
        max_score = 1

    quiz = Knowtionary.objects.create(
        content=library_content,
        description=data.get('description', ''),
        max_score_per_question=max_score
    )

    questions_data = data.get('questions', [])

    if questions_data:
        for q_data in questions_data:
            Question.objects.create(
                quiz=quiz,
                question=q_data.get('question', ''),
                options=q_data.get('options', []),
                correct_option=int(q_data.get('correct_option', 0))
            )
    else:
        Question.objects.create(
            quiz=quiz,
            question="¿Cuál es la capital de Francia?",
            options=["París", "Madrid", "Roma", "Berlín"],
            correct_option=0
        )

        Question.objects.create(
            quiz=quiz,
            question="¿Cuánto es 2 + 2?",
            options=["3", "4", "5", "6"],
            correct_option=1
        )

    serializer = KnowtionarySerializer(quiz)

    return JsonResponse(
        {'success': True, 'quiz': serializer.serialize()},
        status=201
    )

@csrf_exempt
def edit_knowtionary(request, slug=None):
    if request.method not in ['POST', 'PUT', 'PATCH']:
        return HttpResponseNotAllowed(['POST', 'PUT', 'PATCH'])

    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST

        knowtionary = get_object_or_404(Knowtionary, content__slug=slug, content__user=request.user)

        if 'name' in data:
            knowtionary.content.title = data['name']
            knowtionary.content.save()
            
        if 'description' in data:
            knowtionary.description = data['description']
        
        if 'max_score_per_question' in data:
            try:
                knowtionary.max_score_per_question = int(data['max_score_per_question'])
            except ValueError:
                pass

        knowtionary.save()
        serializer = KnowtionarySerializer(knowtionary)
        return JsonResponse({'success': True, 'quiz': serializer.serialize()}, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def delete_knowtionary(request, slug):
    if request.method not in ['POST', 'DELETE']:
        return HttpResponseNotAllowed(['POST', 'DELETE'])

    quiz = get_object_or_404(Knowtionary, content__slug=slug, content__user=request.user)
    library_content = quiz.content
    quiz.delete()
    library_content.delete()

    return JsonResponse({'message': 'Cuestionario eliminado correctamente'}, status=200)

@csrf_exempt
def toggle_favorite(request, slug):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    quiz = get_object_or_404(Knowtionary, content__slug=slug, content__user=request.user)
    quiz.content.is_favorite = not quiz.content.is_favorite
    quiz.content.save()

    serializer = KnowtionarySerializer(quiz)
    return JsonResponse(serializer.serialize(), safe=False)


def play_knowtionary(request, slug):
    return JsonResponse({'message': 'Play mode ready from frontend!'})


def knowtionary_score(request, slug):
    return JsonResponse({'message': 'Score logic handled in frontend!'})