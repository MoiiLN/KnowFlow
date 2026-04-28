import json

from django.http import HttpResponseBadRequest, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from library.models import LibraryContent
from .models import Note
from .serializers import NoteSerializer

def note_list(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    # Filter by user via the content relationship
    notes = Note.objects.filter(content__user=request.user)

    serializer = NoteSerializer(notes)
    return JsonResponse(serializer.serialize(), safe=False)


def note_detail(request, slug):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    # Filter by user via the content relationship
    note = get_object_or_404(Note, content__slug=slug, content__user=request.user)

    serializer = NoteSerializer(note)
    return JsonResponse(serializer.serialize(), safe=False)


@csrf_exempt
def add_note(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON')

    # Find the library content to link to
    library_content = get_object_or_404(
        LibraryContent, id=data.get('library_content_id'), user=request.user
    )

    note = Note.objects.create(
        content=library_content,
        text=data.get('text', ''),
    )

    serializer = NoteSerializer(note)
    return JsonResponse(serializer.serialize(), status=201)


@csrf_exempt
def edit_note(request, slug):
    if request.method not in ['PUT', 'PATCH']:
        return HttpResponseNotAllowed(['PUT', 'PATCH'])

    note = get_object_or_404(Note, content__slug=slug, content__user=request.user)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON')

    if 'text' in data:
        note.text = data['text']
        note.save()

    serializer = NoteSerializer(note)
    return JsonResponse(serializer.serialize(), safe=False)
