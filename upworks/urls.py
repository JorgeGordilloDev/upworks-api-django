from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView, TokenBlacklistView
)

from apps.users.views import Login, Logout


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/logout/', Logout.as_view(), name = 'logout'),
    path('api/v1/login/',Login.as_view(), name = 'login'),

    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/v1/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),

    path('api/v1/', include('apps.users.urls'), name='users'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
