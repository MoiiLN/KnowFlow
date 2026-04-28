from shared.serializers import BaseSerializer

class TimerFlowSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'default_minutes': instance.default_minutes,
            'short_break': instance.short_break,
            'long_break': instance.long_break,
            'cycle_before_long_break': instance.cycle_before_long_break,
        }

class StudySessionSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'planned_minutes': instance.planned_minutes,
            'session_type': instance.session_type,
            'completed': instance.completed,
            'started_at': instance.started_at.isoformat() if instance.started_at else None,
            'ended_at': instance.ended_at.isoformat() if instance.ended_at else None,
            'content_id': instance.content_id,
        }
