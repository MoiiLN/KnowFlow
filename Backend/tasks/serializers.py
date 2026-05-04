from shared.serializers import BaseSerializer


class TaskFlowSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'slug': instance.slug,
            'description': instance.description,
            'priority': instance.priority,
            'status': instance.status,
            'completed': instance.completed,
            'due_date': str(instance.due_date) if instance.due_date else None,
            'due_time': instance.due_time.isoformat() if instance.due_time else None,
            'reminder': instance.reminder.isoformat() if instance.reminder else None,
            'created_at': instance.created_at.isoformat(),
            'updated_at': instance.updated_at.isoformat(),
            'finished_at': instance.finished_at.isoformat() if instance.finished_at else None,
        }