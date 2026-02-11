from shared.serializers import BaseSerializer


class TimerFlowSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'slug': instance.slug,
            'description': instance.description,
            'completed': instance.completed,
            'created_at': instance.created_at.isoformat(),
            'finished_at': instance.finished_at.isoformat(),
        }


class StudySessionSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'planned_minutes': instance.planned_minutes,
            'session_type': instance.session_type,  #
            'completed': instance.completed,
            'started_at': instance.started_at.isoformat(),
            'ended_at': instance.ended_at.isoformat(),
        }
