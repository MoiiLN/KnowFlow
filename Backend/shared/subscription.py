from django.http import JsonResponse
from flashcards.models import FlowCard
from knowtionaries.models import Knowtionary
from notes.models import Note
from tasks.models import TaskFlow

FREE_LIMITS = {
    'knowtionaries': 10,
    'flashcards': 10,
    'tasks': 20,
    'notes': 10,
}

def check_user_limit(user, resource_type):
    profile = user.profile

    if profile.is_premium():
        return None

    counters = {
        'knowtionaries': Knowtionary.objects.filter(content__user=user).count(),
        'flashcards': FlowCard.objects.filter(user=user).count(),
        'tasks': TaskFlow.objects.filter(user=user).count(),
        'notes': Note.objects.filter(content__user=user).count(),
    }

    if counters[resource_type] >= FREE_LIMITS[resource_type]:
        return JsonResponse(
            {
                'success': False,
                'error': f'Has alcanzado el límite gratuito de {FREE_LIMITS[resource_type]} {resource_type}. Actualiza a Premium para más espacio.'
            },
            status=403
        )

    return None