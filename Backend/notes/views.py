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

    notes = Note.objects.all()

    serializer = NoteSerializer()

    return JsonResponse(serializer.serialize_queryset(notes), safe=False)


def note_detail(request, slug):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    note = get_object_or_404(Note, slug=slug)

    serializer = NoteSerializer()

    return JsonResponse(serializer.serialize_instance(note))


@csrf_exempt
def add_note(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON')

    library_content = get_object_or_404(
        LibraryContent, id=data.get('library_content_id')
    )

    note = Note.objects.create(
        
        library=library_content,
        title=data['title'],
        slug=data['slug'],
        content=data['content'],
    )

    serializer = NoteSerializer()

    return JsonResponse(serializer.serialize_instance(note), status=201)


@csrf_exempt
def edit_note(request, slug):
    if request.method not in ['PUT', 'PATCH']:
        return HttpResponseNotAllowed(['PUT', 'PATCH'])

    note = get_object_or_404(Note, slug=slug)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON')

    for field in ['title', 'slug', 'content']:
        if field in data:
            setattr(note, field, data[field])

    note.save()

    serializer = NoteSerializer()

    return JsonResponse(serializer.serialize_instance(note))
