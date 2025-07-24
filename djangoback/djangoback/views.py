# views.py
import os
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from rest_framework import viewsets, permissions, status, serializers
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Presentation, PopQuiz, PresentationParticipant, RegisteredUser, MediaFile
from .serializers import (
    PresentationSerializer,
    PopQuizSerializer,
    MediaFileSerializer
)
from dotenv import load_dotenv

from .utils import upload_images_to_oss, generate_quiz_from_images

import json

load_dotenv()  # 读取根目录的 .env 文件

poppler_path = os.getenv('POPPLER_PATH')

# 演讲列表
class PresentationViewSet(viewsets.ModelViewSet):
    queryset = Presentation.objects.all().order_by('-created_at')
    serializer_class = PresentationSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'uuid'

    def get_queryset(self):
        user = self.request.user
        return Presentation.objects.filter(
            Q(presenter=user) | Q(participants__user=user)
        ).distinct().order_by('-created_at')

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

from urllib.parse import unquote
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from tempfile import NamedTemporaryFile
import os
import uuid
import io
from pdf2image import convert_from_path  # 更适合转换 PDF
from .models import Image  # 你定义的 Image 模型

class MediaFileViewSet(viewsets.ModelViewSet):
    queryset = MediaFile.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MediaFileSerializer
    lookup_field = 'uuid'

    def perform_create(self, serializer):
        print('Request data:', self.request.data)

        presentation_uuid = self.request.data.get('presentation_uuid')
        if not presentation_uuid:
            raise serializers.ValidationError("缺少 presentation_uuid")

        presentation = get_object_or_404(Presentation, uuid=presentation_uuid)

        if presentation.presenter != self.request.user:
            raise serializers.ValidationError("无权为该演讲上传媒体")

        uploaded_file = self.request.FILES.get('file')
        if not uploaded_file:
            raise serializers.ValidationError("未提供文件")

        # 安全文件名
        decoded_name = unquote(uploaded_file.name)
        safe_name = os.path.basename(decoded_name)

        # 保存 MediaFile 实例
        media_instance = serializer.save(title=safe_name, presentation=presentation)

        # 临时保存上传文件
        with NamedTemporaryFile(delete=False, suffix=os.path.splitext(safe_name)[1]) as temp_file:
            for chunk in uploaded_file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        file_ext = os.path.splitext(safe_name)[1].lower()

        try:
            if file_ext == ".pdf":
                self._convert_pdf_to_images(temp_file_path, presentation, "pdf")
            elif file_ext == ".pptx":
                self._convert_pptx_to_images(temp_file_path, presentation, "pptx")
            else:
                print("暂不支持该格式")
        finally:
            os.remove(temp_file_path)

    def _convert_pdf_to_images(self, filepath, presentation, file_type):
        # 使用 pdf2image 转换每一页为 PIL.Image
        pages = convert_from_path(filepath, poppler_path=poppler_path)
        for i, page in enumerate(pages, start=1):
            img_io = io.BytesIO()
            page.save(img_io, format="PNG")
            img_io.seek(0)

            image_filename = f"{uuid.uuid4()}.png"
            image_path = f"converted_images/{image_filename}"
            default_storage.save(image_path, ContentFile(img_io.read()))

            Image.objects.create(
                presentation=presentation,
                image_file=image_path,
                file_type=file_type,
                page_number=i
            )

    def _convert_pptx_to_images(self, filepath, presentation, file_type):
        # 简化版：将 PPTX 每一页截图为图片
        from .utils import pptx_to_pdf
        # 将pptx转为pdf然后复用上面的逻辑

        # 转成 PDF
        pdf_path = filepath.replace('.pptx', '.pdf')
        pptx_to_pdf(filepath, pdf_path)

        # 复用 PDF 转换逻辑
        self._convert_pdf_to_images(pdf_path, presentation, file_type)

        os.remove(pdf_path)  # 清理转换后的PDF

    def get_queryset(self):
        queryset = super().get_queryset()
        presentation_uuid = self.request.query_params.get('presentation')
        if presentation_uuid:
            queryset = queryset.filter(presentation__uuid=presentation_uuid)
        return queryset

# 以下为自定义视图逻辑
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


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


class GenerateQuizAPIView(APIView):
    """
    POST /api/generate-quiz/?presentation_uuid=xxx
    """

    def post(self, request):
        presentation_uuid = request.query_params.get("presentation_uuid")
        if not presentation_uuid:
            return Response({"detail": "缺少 presentation_uuid"}, status=400)

        try:
            presentation = Presentation.objects.get(uuid=presentation_uuid)
        except Presentation.DoesNotExist:
            return Response({"detail": "演讲不存在"}, status=404)

        # 获取演讲对应的所有图片路径
        images = presentation.images.all()
        local_paths = [img.image.path for img in images if img.image]

        # 1. 上传到 OSS
        image_urls = upload_images_to_oss(local_paths)

        # 2. 调用 AI 生成题目
        try:
            quiz_data = generate_quiz_from_images(image_urls)
            quiz_list = json.loads(quiz_data)  # 需确保 AI 返回为合法 JSON
        except Exception as e:
            return Response({"detail": str(e)}, status=500)

        # 3. 存储题目
        for i, q in enumerate(quiz_list):
            PopQuiz.objects.create(
                question_type='choice',
                question_text=q['question'],
                options=q['options'],
                correct_answers=[q['answer']],
                is_multiple=False,
                quiz_index=i,
                presentation=presentation,
            )

        return Response({"detail": "题目生成成功"}, status=status.HTTP_201_CREATED)

