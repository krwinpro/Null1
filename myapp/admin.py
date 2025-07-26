from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.contrib import messages
from .models import UserProfile, Category, Post, PostFile, Announcement, BlockedIP

# 1. IP만 차단 (계정은 유지)
def block_ip_only(modeladmin, request, queryset):
    """선택된 사용자들의 IP만 차단 (계정은 유지)"""
    blocked_count = 0
    for user_profile in queryset:
        blocked_ip, created = BlockedIP.objects.get_or_create(
            ip_address=user_profile.ip_address,
            defaults={
                'reason': f'{user_profile.user.username} 사용자 IP 차단',
                'blocked_by': request.user
            }
        )
        if created:
            blocked_count += 1
    
    messages.success(request, f'{blocked_count}개의 IP가 차단되었습니다. (계정은 유지됨)')

block_ip_only.short_description = "🚫 선택된 사용자의 IP만 차단"

# 2. 계정만 삭제 (IP는 차단하지 않음)
def delete_user_only(modeladmin, request, queryset):
    """선택된 사용자만 삭제 (IP는 차단하지 않음)"""
    deleted_users = 0
    deleted_posts = 0
    
    for user_profile in queryset:
        user = user_profile.user
        
        # 사용자의 모든 게시물 삭제
        posts_count = Post.objects.filter(author=user).count()
        Post.objects.filter(author=user).delete()
        deleted_posts += posts_count
        
        # 사용자 삭제 (UserProfile은 CASCADE로 자동 삭제)
        user.delete()
        deleted_users += 1
    
    messages.success(request, f'{deleted_users}명의 사용자와 {deleted_posts}개의 게시물이 삭제되었습니다. (IP는 차단되지 않음)')

delete_user_only.short_description = "👤 선택된 사용자만 삭제 (IP 차단 안함)"

# 3. 계정 삭제 + IP 차단 (재가입 방지)
def delete_user_and_block_ip(modeladmin, request, queryset):
    """선택된 사용자 삭제 + IP 차단으로 재가입 방지"""
    deleted_users = 0
    deleted_posts = 0
    blocked_ips = 0
    
    for user_profile in queryset:
        user = user_profile.user
        username = user.username
        ip_address = user_profile.ip_address
        
        # IP 차단 먼저 처리
        blocked_ip, created = BlockedIP.objects.get_or_create(
            ip_address=ip_address,
            defaults={
                'reason': f'{username} 사용자 탈퇴 + 재가입 방지',
                'blocked_by': request.user
            }
        )
        if created:
            blocked_ips += 1
        
        # 사용자의 모든 게시물 삭제
        posts_count = Post.objects.filter(author=user).count()
        Post.objects.filter(author=user).delete()
        deleted_posts += posts_count
        
        # 사용자 삭제
        user.delete()
        deleted_users += 1
    
    messages.success(request, f'{deleted_users}명의 사용자와 {deleted_posts}개의 게시물이 삭제되고, {blocked_ips}개의 IP가 차단되었습니다.')

delete_user_and_block_ip.short_description = "🔒 사용자 삭제 + IP 차단 (재가입 방지)"

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'get_email', 'ip_address', 'last_login_ip', 
        'join_date', 'get_post_count', 'get_user_status'
    ]
    list_filter = ['join_date']
    search_fields = ['user__username', 'user__email', 'ip_address', 'last_login_ip']
    readonly_fields = ['join_date', 'get_user_info', 'get_post_list']
    
    # 3가지 액션만 등록
    actions = [
        block_ip_only, 
        delete_user_only, 
        delete_user_and_block_ip
    ]
    
    fieldsets = (
        ('사용자 정보', {
            'fields': ('user', 'get_user_info')
        }),
        ('IP 정보', {
            'fields': ('ip_address', 'last_login_ip')
        }),
        ('기타', {
            'fields': ('join_date',)
        }),
        ('게시물 정보', {
            'fields': ('get_post_list',),
            'classes': ('collapse',)
        })
    )
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = '이메일'
    
    def get_post_count(self, obj):
        count = Post.objects.filter(author=obj.user).count()
        return format_html(
            '<span style="color: {};">{}</span>',
            'red' if count > 10 else 'green',
            count
        )
    get_post_count.short_description = '게시물 수'
    
    def get_user_status(self, obj):
        # IP 차단 상태 체크
        if BlockedIP.objects.filter(ip_address=obj.ip_address).exists():
            return format_html('<span style="color: red; font-weight: bold;">IP 차단됨</span>')
        else:
            return format_html('<span style="color: green;">정상</span>')
    get_user_status.short_description = 'IP 상태'
    
    def get_user_info(self, obj):
        # IP 차단 상태 확인
        ip_blocked = BlockedIP.objects.filter(ip_address=obj.ip_address).exists()
        ip_status = '<span style="color: red;">차단됨</span>' if ip_blocked else '<span style="color: green;">정상</span>'
        
        return format_html(
            '''
            <div style="background: #f8f9fa; padding: 10px; border-radius: 5px;">
                <strong>사용자명:</strong> {}<br>
                <strong>이메일:</strong> {}<br>
                <strong>가입일:</strong> {}<br>
                <strong>마지막 로그인:</strong> {}<br>
                <strong>스태프 권한:</strong> {}<br>
                <strong>IP 상태:</strong> {}
            </div>
            ''',
            obj.user.username,
            obj.user.email,
            obj.join_date.strftime('%Y-%m-%d %H:%M:%S'),
            obj.user.last_login.strftime('%Y-%m-%d %H:%M:%S') if obj.user.last_login else '없음',
            '예' if obj.user.is_staff else '아니오',
            ip_status
        )
    get_user_info.short_description = '상세 정보'
    
    def get_post_list(self, obj):
        posts = Post.objects.filter(author=obj.user).order_by('-created_at')[:10]
        if not posts:
            return "게시물이 없습니다."
        
        post_list = []
        for post in posts:
            post_list.append(
                f'<li><strong>{post.title}</strong> ({post.created_at.strftime("%Y-%m-%d")})</li>'
            )
        
        return format_html(
            '<ul style="margin: 0; padding-left: 20px;">{}</ul>',
            ''.join(post_list)
        )
    get_post_list.short_description = '최근 게시물 (최대 10개)'

# IP 차단 해제 액션
def unblock_ip(modeladmin, request, queryset):
    """선택된 IP 차단 해제"""
    count = queryset.count()
    queryset.delete()
    messages.success(request, f'{count}개의 IP 차단이 해제되었습니다.')

unblock_ip.short_description = "🔓 선택된 IP 차단 해제"

@admin.register(BlockedIP)
class BlockedIPAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'reason', 'blocked_date', 'blocked_by']
    list_filter = ['blocked_date', 'blocked_by']
    search_fields = ['ip_address', 'reason']
    readonly_fields = ['blocked_date']
    actions = [unblock_ip]
    
    fieldsets = (
        ('차단 정보', {
            'fields': ('ip_address', 'reason')
        }),
        ('차단 기록', {
            'fields': ('blocked_by', 'blocked_date')
        })
    )

# PostFile 인라인 관리
class PostFileInline(admin.TabularInline):
    model = PostFile
    extra = 0
    readonly_fields = ['uploaded_at', 'get_file_size', 'get_file_type']
    
    def get_file_size(self, obj):
        if obj.file:
            try:
                size = obj.file.size
                if size < 1024:
                    return f"{size} B"
                elif size < 1024*1024:
                    return f"{size/1024:.1f} KB"
                else:
                    return f"{size/(1024*1024):.1f} MB"
            except:
                return "알 수 없음"
        return "파일 없음"
    get_file_size.short_description = '파일 크기'
    
    def get_file_type(self, obj):
        return obj.get_file_type().upper()
    get_file_type.short_description = '파일 타입'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'created_at', 'is_pinned', 'get_author_ip', 'get_file_count']
    list_filter = ['category', 'is_pinned', 'created_at']
    search_fields = ['title', 'content', 'author__username']
    readonly_fields = ['created_at']
    inlines = [PostFileInline]
    
    def get_author_ip(self, obj):
        try:
            profile = UserProfile.objects.get(user=obj.author)
            return profile.ip_address
        except UserProfile.DoesNotExist:
            return "IP 없음"
    get_author_ip.short_description = '작성자 IP'
    
    def get_file_count(self, obj):
        count = obj.postfile_set.count()
        return f"{count}개" if count > 0 else "없음"
    get_file_count.short_description = '첨부파일'

@admin.register(PostFile)
class PostFileAdmin(admin.ModelAdmin):
    list_display = ['post', 'original_name', 'get_file_type', 'get_file_size', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['post__title', 'original_name']
    readonly_fields = ['uploaded_at']
    
    def get_file_type(self, obj):
        return obj.get_file_type().upper()
    get_file_type.short_description = '파일 타입'
    
    def get_file_size(self, obj):
        size = obj.get_file_size()
        if size < 1024:
            return f"{size} B"
        elif size < 1024*1024:
            return f"{size/1024:.1f} KB"
        else:
            return f"{size/(1024*1024):.1f} MB"
    get_file_size.short_description = '파일 크기'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'get_post_count']
    prepopulated_fields = {'slug': ('name',)}
    
    def get_post_count(self, obj):
        count = Post.objects.filter(category=obj).count()
        return count
    get_post_count.short_description = '게시물 수'

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at']

# Django 기본 User 모델 커스터마이징
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = BaseUserAdmin.list_display + ('get_ip_address',)
    
    def get_ip_address(self, obj):
        try:
            profile = UserProfile.objects.get(user=obj)
            return profile.ip_address
        except UserProfile.DoesNotExist:
            return "IP 없음"
    get_ip_address.short_description = 'IP 주소'

# 기존 User admin 등록 해제 후 새로운 것으로 등록
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Admin 사이트 커스터마이징
admin.site.site_header = "DarkWeb 관리자"
admin.site.site_title = "DarkWeb Admin"
admin.site.index_title = "DarkWeb 관리 패널"


