from rest_framework import serializers
from .models import PopQuiz, Presentation, MediaFile


class PopQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = PopQuiz
        fields = '__all__'  # 或者列出你需要的字段

class PresentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presentation
        fields = '__all__'
        read_only_fields = ('id', 'uuid', 'presenter', 'created_at', 'updated_at')

class MediaFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile
        fields = ['id', 'uuid', 'file', 'type', 'title', 'uploaded_at', 'order']