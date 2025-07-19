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
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PopQuizViewSet, RegisterView, LoginView, PresentationListView, UploadMediaFileView
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # 登录（获取access + refresh）
    TokenRefreshView,     # 刷新access
)

router = DefaultRouter()
router.register(r'popquiz', PopQuizViewSet, basename='popquiz')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/presentations/', PresentationListView.as_view(), name='presentations'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/upload-media/', UploadMediaFileView.as_view(), name='upload_media'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
