from shared.serializers import BaseSerializer


class NoteSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        # Note points to LibraryContent via 'content'
        return {
            'id': instance.pk,
            'title': instance.content.title,
            'slug': instance.content.slug,
            'text': instance.text,
            'file': self.build_url(instance.file.url) if instance.file else None,
            'created_at': instance.content.created_at.isoformat(),
            'updated_at': instance.content.updated_at.isoformat(),
        }
