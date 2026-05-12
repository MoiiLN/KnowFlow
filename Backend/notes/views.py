import json

from django.http import HttpResponseBadRequest, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
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

    # VALIDACIÓN DE SUSCRIPCIÓN
    from shared.subscription import check_user_limit
    limit_response = check_user_limit(request.user, 'notes')
    if limit_response:
        return limit_response

    # Get library_content_id
    content_id = data.get('library_content_id')

    library_content = None

    # If a valid ID is provided, we use it
    if content_id and content_id != '1':  # Avoid the mock '1'
        library_content = LibraryContent.objects.filter(
            id=content_id,
            user=request.user
        ).first()

    if not library_content:
        from library.models import Library
        library_id = data.get('library_id')
        
        if library_id:
            print(f"DEBUG: Buscando librería con ID: {library_id}")
            library = Library.objects.filter(id=library_id, user=request.user).first()
            if not library:
                print(f"DEBUG: No se encontró librería {library_id} para el usuario {request.user.id}")
        else:
            print("DEBUG: No se proporcionó library_id, usando la primera disponible")
            library = Library.objects.filter(user=request.user).first()

        if not library:
            import uuid
            unique_suffix = str(uuid.uuid4())[:8]

            library = Library.objects.create(
                user=request.user,
                name=f"General ({request.user.username})",
                slug=f"general-{request.user.username}-{unique_suffix}",
                description="Librería generada automáticamente para tus notas."
            )

        import uuid
        try:
            library_content = LibraryContent.objects.create(
                user=request.user,
                library=library,
                title=data.get('title', 'Nueva Nota'),
                slug=data.get('slug') or f"nota-{str(uuid.uuid4())[:8]}"
            )
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                return JsonResponse({'success': False, 'error': 'Ya existe una nota con ese título en esta librería.'}, status=400)
            raise e

    try:
        note = Note.objects.create(
            content=library_content,
            text=data.get('content') or data.get('text', ''),
            file=request.FILES.get('file')
        )
        
        serializer = NoteSerializer(note)
        return JsonResponse(serializer.serialize(), status=201, safe=False)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@csrf_exempt
def edit_note(request, slug):
    # Allow POST as well for FormData compatibility
    if request.method not in ['POST', 'PUT', 'PATCH']:
        return HttpResponseNotAllowed(['POST', 'PUT', 'PATCH'])

    note = get_object_or_404(Note, content__slug=slug, content__user=request.user)

    if request.content_type == 'application/json':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest('Invalid JSON')
    else:
        data = request.POST

    # Update related LibraryContent title if provided
    if 'title' in data:
        note.content.title = data['title']
        note.content.save()

    # Update text/content
    if 'text' in data:
        note.text = data['text']
    elif 'content' in data:
        note.text = data['content']
    
    # Update file if provided
    if request.FILES.get('file'):
        note.file = request.FILES['file']
        
    note.save()

    serializer = NoteSerializer(note)
    return JsonResponse(serializer.serialize(), safe=False)


@csrf_exempt
def delete_note(request, slug):
    if request.method not in ['POST', 'DELETE']:
        return HttpResponseNotAllowed(['POST', 'DELETE'])

    note = get_object_or_404(Note, content__slug=slug, content__user=request.user)
    library_content = note.content
    note.delete()
    library_content.delete()

    return JsonResponse({'message': 'Nota eliminada correctamente'}, status=200)


@csrf_exempt
def toggle_favorite(request, slug):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    note = get_object_or_404(Note, content__slug=slug, content__user=request.user)
    note.favorite = not note.favorite
    note.save()

    serializer = NoteSerializer(note)
    return JsonResponse(serializer.serialize(), safe=False)
