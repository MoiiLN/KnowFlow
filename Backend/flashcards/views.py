import json

from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import FlowCard
from .serializers import FlowCardSerializer
from library.models import LibraryContent

def flowcard_list(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    flowcards = FlowCard.objects.filter(user=request.user)
    serializer = FlowCardSerializer(flowcards)

    return JsonResponse(
        serializer.serialize(),
        safe=False
    )

def flowcard_detail(request, slug):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    flowcard = get_object_or_404(
        FlowCard,
        user=request.user,
        slug=slug
    )

    serializer = FlowCardSerializer(flowcard)
    return JsonResponse(serializer.serialize(), safe=False)


@csrf_exempt
def add_flowcard(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON')

    library_content_id = data.get('library_content_id')
    library_content = None
    if library_content_id and library_content_id != '1':
        library_content = get_object_or_404(
            LibraryContent,
            id=library_content_id,
            user=request.user
        )

    if not library_content:
        from library.models import Library
        library_id = data.get('library_id')
        if library_id:
            library = Library.objects.filter(id=library_id, user=request.user).first()
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
        library_content = LibraryContent.objects.create(
            user=request.user,
            library=library,
            title=data.get('name') or data.get('term', 'Nueva Flashcard'),
            slug=data.get('slug') or f"flashcard-{str(uuid.uuid4())[:8]}"
        )

    flowcard = FlowCard.objects.create(
        user=request.user,
        library=library_content,
        name=data['name'],
        slug=data['slug'],
        term=data['term'],
        definition=data['definition'],
    )

    serializer = FlowCardSerializer(flowcard)
    return JsonResponse(
        serializer.serialize(),
        status=201
    )


@csrf_exempt
def edit_flowcard(request, slug):
    if request.method not in ['PUT', 'PATCH']:
        return HttpResponseNotAllowed(['PUT', 'PATCH'])

    flowcard = get_object_or_404(
        FlowCard,
        user=request.user,
        slug=slug
    )

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON')

    for field in ['name', 'slug', 'term', 'definition']:
        if field in data:
            setattr(flowcard, field, data[field])

    flowcard.save()

    serializer = FlowCardSerializer(flowcard)
    return JsonResponse(serializer.serialize(), safe=False)


def play_flowcard(request, slug):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    flowcard = get_object_or_404(
        FlowCard,
        user=request.user,
        slug=slug
    )

    return JsonResponse({
        'id': flowcard.pk,
        'term': flowcard.term,
        'definition': flowcard.definition,
    })
