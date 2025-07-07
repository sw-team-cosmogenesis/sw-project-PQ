from rest_framework import viewsets
from .models import PopQuiz
from .serializers import PopQuizSerializer

class PopQuizViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PopQuiz.objects.all()
    serializer_class = PopQuizSerializer
