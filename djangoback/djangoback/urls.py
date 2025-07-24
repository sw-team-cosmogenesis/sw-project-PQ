"""
URL configuration for djangoback project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include
from rest_framework.routers import DefaultRouter

from .views import PopQuizViewSet, RegisterView, LoginView, PresentationViewSet, MediaFileViewSet, GenerateQuizAPIView
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,     # 刷新access
)


# ViewSet 视图注册如下
router = DefaultRouter()
router.register(r'popquiz', PopQuizViewSet, basename='popquiz')
router.register(r'presentations', PresentationViewSet, basename='presentations')
router.register(r'upload-media', MediaFileViewSet, basename='media_upload')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    # APIView 视图注册如下
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("api/generate-quiz/", GenerateQuizAPIView.as_view(), name="generate-quiz"),
]

# 媒体文件路径
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
