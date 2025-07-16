from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404

from .models import PopQuiz, RegisteredUser, Presentation, PresentationParticipant
from .serializers import PopQuizSerializer, PresentationSerializer


class PopQuizViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PopQuiz.objects.all()
    serializer_class = PopQuizSerializer

class PresentationListView(APIView):
    def get(self, request):
        presentations = Presentation.objects.all().order_by('-created_at')
        serializer = PresentationSerializer(presentations, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def presentation_detail(request, uuid):
    presentation = get_object_or_404(Presentation, uuid=uuid)
    # 查询用户身份
    try:
        participant = PresentationParticipant.objects.get(user=request.user, presentation=presentation)
        role = participant.role
    except PresentationParticipant.DoesNotExist:
        role = 'viewer' if presentation.is_public else None

    # 返回不同身份的数据
    return Response({
        'presentation': PresentationSerializer(presentation).data,
        'role': role
    })

@permission_classes([AllowAny])
class RegisterView(APIView):
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