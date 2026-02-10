from shared.serializers import BaseSerializer


class ProfileSerializer(BaseSerializer):
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
