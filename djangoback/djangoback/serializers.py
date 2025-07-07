from rest_framework import serializers
from .models import PopQuiz

class PopQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = PopQuiz
        fields = '__all__'  # 或者列出你需要的字段
