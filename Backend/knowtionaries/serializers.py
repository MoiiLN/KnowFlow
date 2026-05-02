from shared.serializers import BaseSerializer


class KnowtionarySerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        questions = []
        for q in instance.questions.all():
            questions.append({
                'id': q.id,
                'question': q.question,
                'options': q.options if isinstance(q.options, list) else [],
                'correct_option': q.correct_option
            })
            
        return {
            'id': instance.pk,
            'name': instance.content.title,
            'slug': instance.content.slug,
            'description': instance.description,
            'max_score_per_question': getattr(instance, 'max_score_per_question', 1),
            'questions_count': instance.questions.count(),
            'avg_score': 0,
            'questions': questions,
            'is_owner': True,
            'author': instance.content.user.username,
            'created_at': instance.created_at.isoformat(),
            'updated_at': instance.updated_at.isoformat(),
            'favorite': instance.content.is_favorite,
        }
