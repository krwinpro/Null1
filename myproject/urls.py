from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('whereisadminssite-dgdb-1111/', admin.site.urls),
    path('', include('myapp.urls')),
]

# 개발 서버에서 미디어 파일 서빙 (이 부분이 중요!)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
