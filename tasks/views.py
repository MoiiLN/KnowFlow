from shared.decorators import require_http_methods

from .models import TaskFlow
from .serializers import TaskFlowSerializer


@require_http_methods('GET')
def task_list(request):
    tasks = TaskFlow.objects.all()
    serializer = TaskFlowSerializer(tasks)
    return serializer.json_response()
