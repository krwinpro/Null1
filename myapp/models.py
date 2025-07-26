from django.db import models
from django.contrib.auth.models import User
import os
from datetime import datetime

def get_upload_path(instance, filename):
    """파일 업로드 경로를 동적으로 생성"""
    # 현재 날짜로 폴더 구조 생성
    now = datetime.now()
    year = now.strftime('%Y')
    month = now.strftime('%m')
    day = now.strftime('%d')
    
    # 파일 확장자 추출
    ext = os.path.splitext(filename)[1].lower()
    
    # 파일 타입별 폴더 분류
    if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg']:
        folder = 'images'
    elif ext in ['.mp4', '.avi', '.mov', '.webm', '.mkv', '.flv', '.wmv']:
        folder = 'videos'
    elif ext in ['.mp3', '.wav', '.ogg', '.m4a', '.aac', '.flac']:
        folder = 'audio'
    elif ext in ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']:
        folder = 'documents'
    elif ext in ['.zip', '.rar', '.7z', '.tar', '.gz']:
        folder = 'archives'
    elif ext in ['.exe', '.msi', '.deb', '.rpm']:
        folder = 'executables'
    elif ext in ['.py', '.js', '.html', '.css', '.php', '.java', '.cpp', '.c', '.h']:
        folder = 'code'
    else:
        folder = 'others'
    
    # 최종 경로: uploads/타입/년/월/일/파일명
    return f'uploads/{folder}/{year}/{month}/{day}/{filename}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    join_date = models.DateTimeField(auto_now_add=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_pinned = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    def get_files(self):
        """게시물에 첨부된 모든 파일 반환"""
        return self.postfile_set.all()
    
    def has_files(self):
        """파일이 첨부되어 있는지 확인"""
        return self.postfile_set.exists()

class PostFile(models.Model):
    """게시물 첨부파일 모델 (여러 파일 지원)"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_upload_path)
    original_name = models.CharField(max_length=255)  # 원본 파일명 저장
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.post.title} - {self.original_name}"
    
    def get_file_size(self):
        """파일 크기 반환"""
        try:
            return self.file.size
        except:
            return 0
    
    def get_file_extension(self):
        """파일 확장자 반환"""
        if self.file:
            return os.path.splitext(self.file.name)[1].lower()
        return ''
    
    def get_file_type(self):
        """파일 타입 반환"""
        ext = self.get_file_extension()
        
        if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.ico', '.tiff', '.tif']:
            return "image"
        elif ext in ['.mp4', '.avi', '.mov', '.webm', '.mkv', '.flv', '.wmv', '.m4v', '.3gp', '.ogv']:
            return "video"
        elif ext in ['.mp3', '.wav', '.ogg', '.m4a', '.aac', '.flac', '.wma']:
            return "audio"
        elif ext in ['.pdf']:
            return "pdf"
        elif ext in ['.txt', '.md', '.log', '.cfg', '.ini', '.conf']:
            return "text"
        elif ext in ['.doc', '.docx']:
            return "document"
        elif ext in ['.xls', '.xlsx']:
            return "spreadsheet"
        elif ext in ['.ppt', '.pptx']:
            return "presentation"
        elif ext in ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz']:
            return "archive"
        elif ext in ['.exe', '.msi', '.deb', '.rpm', '.dmg', '.app']:
            return "executable"
        elif ext in ['.py', '.js', '.html', '.css', '.php', '.java', '.cpp', '.c', '.h', '.json', '.xml', '.sql']:
            return "code"
        else:
            return "file"

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class BlockedIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    reason = models.CharField(max_length=200, default="관리자에 의한 차단")
    blocked_date = models.DateTimeField(auto_now_add=True)
    blocked_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"차단된 IP: {self.ip_address}"

    class Meta:
        verbose_name = "차단된 IP"
        verbose_name_plural = "차단된 IP 목록"


