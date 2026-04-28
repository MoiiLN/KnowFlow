from shared.serializers import BaseSerializer


class KnowtionarySerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        # Knowtionary points to LibraryContent via 'content'
        return {
            'id': instance.pk,
            'title': instance.content.title,
            'slug': instance.content.slug,
            'description': instance.description,
            'created_at': instance.created_at.isoformat(),
            'updated_at': instance.updated_at.isoformat(),
        }
