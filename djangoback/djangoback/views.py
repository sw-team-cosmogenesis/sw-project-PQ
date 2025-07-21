# views.py
import os
from urllib.parse import unquote

from django.db.models import Q
from rest_framework import viewsets, permissions, status, serializers
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password

from .models import Presentation, PopQuiz, PresentationParticipant, RegisteredUser, MediaFile
from .serializers import (
    PresentationSerializer,
    PopQuizSerializer,
    MediaFileSerializer
)

# 演讲列表
class PresentationViewSet(viewsets.ModelViewSet):
    queryset = Presentation.objects.all().order_by('-created_at')
    serializer_class = PresentationSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'uuid'

    # def get_queryset(self):
    #     user = self.request.user
    #     return Presentation.objects.filter(
    #         Q(presenter=user) | Q(participants__user=user)
    #     ).distinct().order_by('-created_at')

    def perform_create(self, serializer):
        presentation = serializer.save(presenter=self.request.user)
        PresentationParticipant.objects.create(
            user=self.request.user,
            presentation=presentation,
            role='presenter'
        )

# 上传文件视图
class PopQuizViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PopQuiz.objects.all()
    serializer_class = PopQuizSerializer
    lookup_field = 'uuid'

class MediaFileViewSet(viewsets.ModelViewSet):
    queryset = MediaFile.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MediaFileSerializer
    lookup_field = 'uuid'

    from urllib.parse import unquote
    import os

    def perform_create(self, serializer):
        print('Request data:', self.request.data)

        presentation_uuid = self.request.data.get('presentation_uuid')
        if not presentation_uuid:
            raise serializers.ValidationError("缺少 presentation_uuid")

        presentation = get_object_or_404(Presentation, uuid=presentation_uuid)

        if presentation.presenter != self.request.user:
            raise serializers.ValidationError("无权为该演讲上传媒体")

        # 文件安全处理
        uploaded_file = self.request.FILES.get('file')
        decoded_name = unquote(uploaded_file.name)

        serializer.save(title=os.path.basename(decoded_name), presentation=presentation)

    def get_queryset(self):
        queryset = super().get_queryset()
        presentation_uuid = self.request.query_params.get('presentation')  # ← 正确方式
        if presentation_uuid:
            queryset = queryset.filter(presentation__uuid=presentation_uuid)
        return queryset

# 以下为自定义视图逻辑
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated


# 注册视图
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if RegisteredUser.objects.filter(email=email).exists():
            return Response({"detail": "邮箱已存在"}, status=status.HTTP_400_BAD_REQUEST)

        user = RegisteredUser.objects.create(
            username=email,
            email=email,
            password=make_password(password)
        )
        return Response({"detail": "注册成功"}, status=status.HTTP_201_CREATED)

# 登录视图
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = RegisteredUser.objects.get(email=email)
        except RegisteredUser.DoesNotExist:
            return Response({'detail': '邮箱不存在'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({'detail': '密码错误'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'token': str(refresh.access_token),
            'user_id': user.id,
            'email': user.email,
        })

