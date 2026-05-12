import json
from django.shortcuts import render
from shared.decorators import require_http_methods
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt

from .models import Library, LibraryContent
from .serializers import LibrarySerializer, LibraryContentSerializer

@require_http_methods('GET')
def library_list(request):
    # Filter by user
    libraries = Library.objects.filter(user=request.user)
    serializer = LibrarySerializer(libraries)
    return JsonResponse(serializer.serialize(), safe=False)


@require_http_methods('GET')
def library_detail(request, library_id):
    try:
        library = Library.objects.get(id=library_id, user=request.user)
    except Library.DoesNotExist:
        return JsonResponse({'error': 'Library not found'}, status=404)

    serializer = LibrarySerializer(library)
    return JsonResponse(serializer.serialize(), safe=False)


@csrf_exempt
@require_http_methods('POST')
def create_library(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Authentication required'}, status=401)

    try:
        # Check if data is JSON or Form
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST

        from shared.subscription import check_user_limit
        limit_response = check_user_limit(request.user, 'libraries')
        if limit_response:
            return limit_response

        name = data.get('name')
        if not name:
            return JsonResponse({'success': False, 'error': 'Name is required'}, status=400)
            
        description = data.get('description', '')
        
        import uuid
        slug = data.get('slug') or f"{slugify(name)}-{str(uuid.uuid4())[:8]}"
        
        library = Library.objects.create(
            user=request.user,
            name=name,
            slug=slug,
            description=description
        )
        
        serializer = LibrarySerializer(library)
        return JsonResponse({'success': True, 'library': serializer.serialize()}, status=201)
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        error_msg = str(e)
        if "UNIQUE constraint failed" in error_msg:
            error_msg = "Ya tienes una librería con ese nombre. Por favor, elige uno diferente."
        
        return JsonResponse({'success': False, 'error': error_msg}, status=400)


@csrf_exempt
@require_http_methods('PUT', 'PATCH', 'POST')
def edit_library(request, library_id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Authentication required'}, status=401)

    try:
        library = Library.objects.get(id=library_id, user=request.user)
    except Library.DoesNotExist:
        return JsonResponse({'error': 'Library not found'}, status=404)

    try:
        data = json.loads(request.body)
        
        if 'name' in data:
            library.name = data['name']
        if 'description' in data:
            library.description = data['description']
        if 'slug' in data:
            library.slug = data['slug']
            
        library.save()
        
        serializer = LibrarySerializer(library)
        return JsonResponse(serializer.serialize(), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods('DELETE', 'POST')
def delete_library(request, library_id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Authentication required'}, status=401)

    try:
        print(f"DEBUG: Intentando borrar librería ID: {library_id} para usuario: {request.user.username} (ID: {request.user.id})")
        library = Library.objects.get(id=library_id, user=request.user)
    except Library.DoesNotExist:
        print(f"DEBUG: Librería {library_id} no encontrada para el usuario {request.user.id}")
        return JsonResponse({'error': 'Library not found'}, status=404)

    library.delete()
    return JsonResponse({'success': True, 'message': 'Library deleted successfully'}, status=200)

@csrf_exempt
def run_migrations(request):
    from django.core.management import call_command
    from io import StringIO
    out = StringIO()
    try:
        call_command('makemigrations', 'library', stdout=out)
        call_command('migrate', 'library', stdout=out)
        return JsonResponse({'success': True, 'output': out.getvalue()})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e), 'output': out.getvalue()})