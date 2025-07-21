from rest_framework import serializers
from .models import PopQuiz, Presentation, MediaFile


class PopQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = PopQuiz
        fields = '__all__'  # 或者列出你需要的字段

class PresentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presentation
        fields = [
            'uuid',
            'title',
            'description',
            'presenter',
            'scheduled_time',
            'duration_minutes',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ('uuid', 'presenter', 'created_at', 'updated_at')

class MediaFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile
        fields = [
            'uuid',
            'presentation',
            'file',
            'title',
            'uploaded_at',
            'order'
        ]
        read_only_fields = ['uuid', 'presentation', 'uploaded_at']