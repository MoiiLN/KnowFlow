from django.shortcuts import render

from shared.decorators import require_http_methods
from django.http import JsonResponse

from .models import Library
from .serializers import LibrarySerializer


@require_http_methods('GET')
def library_list(request):
    libraries = Library.objects.all()
    serializer = LibrarySerializer(libraries)
    return serializer.json_response()


@require_http_methods('GET')
def library_detail(request, library_id):
    try:
        library = Library.objects.get(id=library_id)
    except Library.DoesNotExist:
        return JsonResponse({'error': 'Library not found'}, status=404)

    serializer = LibrarySerializer(library)
    return serializer.json_response()


@require_http_methods('POST')
def create_library(request):
    print(f"POST create_library: data={dict(request.POST)} user={request.user}")
    serializer = LibrarySerializer(data=request.POST)
    if serializer.is_valid():
        library = serializer.save(user=request.user)
        print(f"Library created ID={library.id}")
        return JsonResponse({'success': True, 'library': serializer.data}, status=201)
    print(f"Serializer errors: {serializer.errors}")
    return JsonResponse({'success': False, 'errors': serializer.errors}, status=400)




@require_http_methods('PUT')
def edit_library(request, library_id):
    try:
        library = Library.objects.get(id=library_id)
    except Library.DoesNotExist:
        return JsonResponse({'error': 'Library not found'}, status=404)

    data = json.loads(request.body)

    serializer = LibrarySerializer(library, data=data)

    if serializer.is_valid():
        library = serializer.save()
        return JsonResponse(serializer.data)

    return JsonResponse(serializer.errors, status=400)


@require_http_methods('DELETE')
def delete_library(request, library_id):
    try:
        library = Library.objects.get(id=library_id)
    except Library.DoesNotExist:
        return JsonResponse({'error': 'Library not found'}, status=404)

    library.delete()
    return JsonResponse({'message': 'Library deleted successfully'}, status=204)