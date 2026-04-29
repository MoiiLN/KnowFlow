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

    # Try to get data from POST (FormData) or JSON body
    if request.content_type == 'application/json':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest('Invalid JSON')
    else:
        data = request.POST

    # Get library_content_id
    content_id = data.get('library_content_id')
    
    library_content = None
    if content_id:
        library_content = LibraryContent.objects.filter(id=content_id, user=request.user).first()
    
    if not library_content:
        # Fallback: find the first available library content for the user
        library_content = LibraryContent.objects.filter(user=request.user).first()
        
    if not library_content:
        # If still no content, we need to create one or error out
        # Let's try to find any library and create a content there
        from library.models import Library
        library = Library.objects.filter(user=request.user).first()
        
        if not library:
            # Auto-create a default library for the user
            import uuid
            unique_suffix = str(uuid.uuid4())[:8]
            library = Library.objects.create(
                user=request.user,
                name=f"General ({request.user.username})",
                slug=f"general-{request.user.username}-{unique_suffix}",
                description="Librería generada automáticamente para tus notas."
            )
            
        library_content = LibraryContent.objects.create(
            user=request.user,
            library=library,
            title=data.get('title', 'Nueva Nota'),
            slug=data.get('slug') or f"nota-{str(uuid.uuid4())[:8]}"
        )

    note = Note.objects.create(
        content=library_content,
        text=data.get('content') or data.get('text', ''),
        file=request.FILES.get('file')
    )

    serializer = NoteSerializer(note)
    return JsonResponse(serializer.serialize(), status=201, safe=False)


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
