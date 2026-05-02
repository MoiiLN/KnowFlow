from shared.serializers import BaseSerializer


class LibrarySerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        contents_data = []
        for content in instance.contents.all():
            item_type = 'unknown'
            item_data = {}
            if hasattr(content, 'flowcard'):
                item_type = 'flashcard'
                item_data = {
                    'term': content.flowcard.term,
                    'definition': content.flowcard.definition,
                    'slug': content.flowcard.slug
                }
            elif hasattr(content, 'note'):
                item_type = 'note'
                item_data = {
                    'text': content.note.text,
                    'favorite': content.note.favorite,
                }
            elif hasattr(content, 'knowtionary'):
                item_type = 'knowtionary'
                item_data = {
                    'description': content.knowtionary.description,
                    'max_score_per_question': content.knowtionary.max_score_per_question,
                    'questions_count': content.knowtionary.questions.count() if hasattr(content.knowtionary, 'questions') else 0
                }

            contents_data.append({
                'id': content.pk,
                'title': content.title,
                'slug': content.slug,
                'created_at': content.created_at.isoformat(),
                'item_type': item_type,
                'data': item_data
            })

        return {
            'id': instance.pk,
            'name': instance.name,
            'slug': instance.slug,
            'description': instance.description,
            'created_at': instance.created_at.isoformat(),
            'updated_at': instance.updated_at.isoformat(),
            'contents': contents_data
        }


class LibraryContentSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'title': instance.title,
            'slug': instance.slug,
            'content_type': instance.content_type,  #
            'is_favorite': instance.is_favorite,
            'created_at': instance.created_at.isoformat(),
            'updated_at': instance.updated_at.isoformat(),
        }
