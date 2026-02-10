from shared.serializers import BaseSerializer


class KnowtionarySerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'slug': instance.slug,
            'description': instance.description,
            'question': instance.question,
            'answer': instance.answer,
            'image': self.build_url(instance.cover.url),
            'created_at': instance.created_at.isoformat(),
        }
