from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import PopQuiz, RegisteredUser, Presentation, PresentationParticipant
from .serializers import PopQuizSerializer, PresentationSerializer, MediaFileSerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from uuid import UUID

class PopQuizViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PopQuiz.objects.all()
    serializer_class = PopQuizSerializer


class PresentationListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        presentations = Presentation.objects.all().order_by('-created_at')
        serializer = PresentationSerializer(presentations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PresentationSerializer(data=request.data)
        if serializer.is_valid():
            # 这里直接传递 presenter 实例给 save()，覆盖掉前端数据
            presentation = serializer.save(presenter=request.user)

            # 自动添加为 presenter 角色的参与者
            PresentationParticipant.objects.create(
                user=request.user,
                presentation=presentation,
                role='presenter'
            )

            return Response(PresentationSerializer(presentation).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def presentation_detail(request, uuid):
    presentation = get_object_or_404(Presentation, uuid=uuid)
    # 查询用户身份
    try:
        participant = PresentationParticipant.objects.get(user=request.user, presentation=presentation)
        role = participant.role
    except PresentationParticipant.DoesNotExist:
        role = 'audience' if presentation.is_public else None

    # 返回不同身份的数据
    return Response({
        'presentation': PresentationSerializer(presentation).data,
        'role': role
    })


class UploadMediaFileView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        presentation_uuid = request.data.get('presentation_uuid')
        if not presentation_uuid:
            return Response({'error': 'presentation_uuid is required'}, status=400)

        try:
            # 确保传入的字符串是合法UUID
            uuid_obj = UUID(presentation_uuid)
        except ValueError:
            return Response({'error': 'Invalid presentation_uuid'}, status=400)

        try:
            presentation = Presentation.objects.get(uuid=uuid_obj)
        except Presentation.DoesNotExist:
            return Response({'error': 'Presentation not found'}, status=404)

        serializer = MediaFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(presentation=presentation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


@permission_classes([AllowAny])
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'detail': '邮箱和密码不能为空'}, status=status.HTTP_400_BAD_REQUEST)

        # 尝试通过邮箱获取用户（假设你的用户模型用 email 登录）
        try:
            user = RegisteredUser.objects.get(email=email)
        except RegisteredUser.DoesNotExist:
            return Response({'detail': '邮箱不存在'}, status=status.HTTP_401_UNAUTHORIZED)

        # 检查密码
        if not user.check_password(password):
            return Response({'detail': '密码错误'}, status=status.HTTP_401_UNAUTHORIZED)

        # 生成 JWT token
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'token': str(refresh.access_token),
            'user_id': user.id,
            'email': user.email,
        })
