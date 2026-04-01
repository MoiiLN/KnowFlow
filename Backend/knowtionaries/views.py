from django.shortcuts import render
from .models import Knowtionary, Question
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from shared.decorators import require_http_methods
from django.http import JsonResponse

from .models import Knowtionary, Question
from .serializers import KnowtionarySerializer

@require_http_methods('GET')
def knowtionary_list(request):
    quizzes = Knowtionary.objects.all()
    serializer = KnowtionarySerializer(quizzes)
    return serializer.json_response()


@require_http_methods('GET')
def knowtionary_detail(request, quiz_id):
    try:
        quiz = Knowtionary.objects.get(id=quiz_id)
    except Knowtionary.DoesNotExist:
        return JsonResponse({'error': 'Knowtionary not found'}, status=404)

    serializer = KnowtionarySerializer(quiz)
    return serializer.json_response()


@require_http_methods('POST')
def add_knowtionary(request):
    data = request.POST
    serializer = KnowtionarySerializer(data=data)

    if serializer.is_valid():
        quiz = serializer.save()
        return JsonResponse(serializer.data, status=201)

    return JsonResponse(serializer.errors, status=400)

def play_knowtionary(request):
    pass


def knowtionary_score(request):
    pass

@require_http_methods('GET')
def question_list(request):
    questions = Question.objects.all()
    serializer = QuestionSerializer(questions)
    return serializer.json_response()


@require_http_methods('POST')
def create_question(request):
    data = request.POST
    serializer = QuestionSerializer(data=data)

    if serializer.is_valid():
        question = serializer.save()
        return JsonResponse(serializer.data, status=201)

    return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def edit_knowtionary(request):
    if request.method == 'PUT':
        data = json.loads(request.body)

        try:
            knowtionary = Knowtionary.objects.get(id=data.get('id'))
        except Knowtionary.DoesNotExist:
            return JsonResponse({'error': 'No existe'}, status=404)

        knowtionary.name = data.get('name', knowtionary.name)
        knowtionary.slug = data.get('slug', knowtionary.slug)
        knowtionary.description = data.get('description', knowtionary.description)
        knowtionary.question = data.get('question', knowtionary.question)
        knowtionary.answer = data.get('answer', knowtionary.answer)

        knowtionary.save()

        return JsonResponse({'message': 'Actualizado'})

    return JsonResponse({'error': 'Método no permitido'}, status=405)