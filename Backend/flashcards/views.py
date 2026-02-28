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
    serializer = FlowCardSerializer()

    return JsonResponse(
        serializer.serialize_queryset(flowcards),
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

    serializer = FlowCardSerializer()
    return JsonResponse(serializer.serialize_instance(flowcard))


@csrf_exempt
def add_flowcard(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON')

    library_content = get_object_or_404(
        LibraryContent,
        id=data.get('library_content_id'),
        user=request.user
    )

    flowcard = FlowCard.objects.create(
        user=request.user,
        library=library_content,
        name=data['name'],
        slug=data['slug'],
        term=data['term'],
        definition=data['definition'],
    )

    serializer = FlowCardSerializer()
    return JsonResponse(
        serializer.serialize_instance(flowcard),
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

    serializer = FlowCardSerializer()
    return JsonResponse(serializer.serialize_instance(flowcard))


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
