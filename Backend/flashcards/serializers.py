from shared.serializers import BaseSerializer


class FlowCardSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'slug': instance.slug,
            'term': instance.term,
            'definition': instance.definition,
            'library_name': instance.library.library.name if instance.library else 'Sin Librería',
            'library_id': instance.library.library.id if instance.library else None,
            'created_at': instance.created_at.isoformat(),
        }
