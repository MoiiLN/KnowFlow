from shared.serializers import BaseSerializer


class FlowCardSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'slug': instance.slug,
            'term': instance.term,
            'definition': instance.definition,
            'created_at': instance.created_at.isoformat(),
        }
