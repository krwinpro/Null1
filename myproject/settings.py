from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'm1J8LQwsm-jMFiGg8ZnxQ9vHHvlO14xZgE-TlLMG3R0gRbdTKfqP'

DEBUG = True

ALLOWED_HOSTS = ['*']  # 모든 호스트 허용

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = []  # 비밀번호 검증 제거

LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'myapp/static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ========== 완전 자유 파일 업로드 설정 ==========

# 파일 크기 제한 완전 제거 (10GB)
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024 * 1024  # 10GB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024 * 1024   # 10GB
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000  # 필드 수 제한 해제

# 파일 업로드 핸들러
FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',  # 큰 파일용
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
]

# 파일 권한 설정
FILE_UPLOAD_PERMISSIONS = 0o777  # 모든 권한
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o777

# 보안 설정 완전 해제
SECURE_CROSS_ORIGIN_OPENER_POLICY = None
SECURE_REFERRER_POLICY = None
SECURE_CONTENT_TYPE_NOSNIFF = False
SECURE_BROWSER_XSS_FILTER = False
X_FRAME_OPTIONS = 'ALLOWALL'

# CSRF 보호 해제 (파일 업로드 문제 해결)
CSRF_COOKIE_SECURE = False
CSRF_USE_SESSIONS = False
CSRF_COOKIE_HTTPONLY = False

# 세션 설정
SESSION_COOKIE_AGE = 86400 * 365  # 1년
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# 타임아웃 설정 (큰 파일 업로드용)
CONN_MAX_AGE = 0

