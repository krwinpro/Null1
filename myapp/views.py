# myapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Post, Announcement, Category, UserProfile, BlockedIP, PostFile
from .forms import UserRegisterForm, PostForm, AnnouncementForm
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
import os

def get_client_ip(request):
    """클라이언트의 실제 IP 주소를 가져오는 함수"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def is_admin(user):
    return user.is_superuser

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    announcements = Announcement.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    return render(request, 'index.html', {'announcements': announcements, 'categories': categories})

def post_list(request, category_slug=None):
    if not request.user.is_authenticated:
        return redirect('login')
    categories = Category.objects.all()
    announcements = Announcement.objects.all().order_by('-created_at')[:5]
    category = None
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        posts = Post.objects.filter(category=category).order_by('-is_pinned', '-created_at')
    else:
        posts = Post.objects.all().order_by('-is_pinned', '-created_at')
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'post_list.html', {
        'posts': page_obj,
        'categories': categories,
        'announcements': announcements,
        'category': category
    })

@login_required
@csrf_exempt  # CSRF 보호 해제
def post_create(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    if request.method == 'POST':
        try:
            # 게시물 생성
            post = Post.objects.create(
                title=request.POST.get('title', '제목 없음'),
                content=request.POST.get('content', ''),
                author=request.user,
                category=category
            )
            
            # 여러 파일 처리 (request.FILES에서 직접)
            files = request.FILES.getlist('files')
            uploaded_count = 0
            
            for file in files:
                if file and file.size > 0:
                    try:
                        post_file = PostFile.objects.create(
                            post=post,
                            file=file,
                            original_name=file.name
                        )
                        uploaded_count += 1
                        print(f"파일 업로드 성공: {file.name} ({file.size} bytes)")
                    except Exception as file_error:
                        print(f"파일 업로드 실패: {file.name} - {str(file_error)}")
                        continue
            
            if uploaded_count > 0:
                messages.success(request, f'게시물이 작성되었습니다! ({uploaded_count}개 파일 업로드됨)')
            else:
                messages.success(request, '게시물이 작성되었습니다.')
            
            return redirect('post_detail', post_id=post.id)
            
        except Exception as e:
            messages.error(request, f'게시물 작성 중 오류: {str(e)}')
            print(f"게시물 작성 오류: {str(e)}")
    
    form = PostForm(initial={'category': category})
    return render(request, 'post_create.html', {'form': form, 'category': category})

@login_required
@user_passes_test(is_admin)
def announcement_create(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = request.user
            announcement.save()
            messages.success(request, '공지가 작성되었습니다.')
            return redirect('home')
    else:
        form = AnnouncementForm()
    return render(request, 'post_create.html', {'form': form})

def register(request):
    client_ip = get_client_ip(request)
    
    # IP 차단 체크
    blocked_ip = BlockedIP.objects.filter(ip_address=client_ip).first()
    if blocked_ip:
        messages.error(request, f'차단된 IP에서는 회원가입을 할 수 없습니다. (사유: {blocked_ip.reason})')
        return redirect('login')
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            UserProfile.objects.create(
                user=user, 
                ip_address=client_ip,
                last_login_ip=client_ip
            )
            messages.success(request, '회원가입이 완료되었습니다.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    client_ip = get_client_ip(request)
    
    # IP 차단 체크
    blocked_ip = BlockedIP.objects.filter(ip_address=client_ip).first()
    if blocked_ip:
        messages.error(request, f'차단된 IP에서는 로그인을 할 수 없습니다. (사유: {blocked_ip.reason})')
        return render(request, 'login.html')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # 로그인 IP 업데이트
            try:
                profile = UserProfile.objects.get(user=user)
                profile.last_login_ip = client_ip
                profile.save()
            except UserProfile.DoesNotExist:
                # 프로필이 없는 경우 생성
                UserProfile.objects.create(
                    user=user,
                    ip_address=client_ip,
                    last_login_ip=client_ip
                )
            
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, '아이디 또는 비밀번호가 잘못되었습니다.')
    return render(request, 'login.html')

@login_required
@csrf_exempt  # CSRF 보호 해제
def post_create_general(request):
    """카테고리를 선택할 수 있는 일반 글쓰기 페이지"""
    if request.method == 'POST':
        try:
            # 카테고리 가져오기
            category_id = request.POST.get('category')
            if not category_id:
                messages.error(request, '카테고리를 선택해주세요.')
                return render(request, 'post_create.html', {'form': PostForm(), 'is_general': True})
            
            category = get_object_or_404(Category, id=category_id)
            
            # 게시물 생성
            post = Post.objects.create(
                title=request.POST.get('title', '제목 없음'),
                content=request.POST.get('content', ''),
                author=request.user,
                category=category
            )
            
            # 여러 파일 처리
            files = request.FILES.getlist('files')
            uploaded_count = 0
            
            for file in files:
                if file and file.size > 0:
                    try:
                        post_file = PostFile.objects.create(
                            post=post,
                            file=file,
                            original_name=file.name
                        )
                        uploaded_count += 1
                        print(f"파일 업로드 성공: {file.name} ({file.size} bytes)")
                    except Exception as file_error:
                        print(f"파일 업로드 실패: {file.name} - {str(file_error)}")
                        continue
            
            if uploaded_count > 0:
                messages.success(request, f'게시물이 작성되었습니다! ({uploaded_count}개 파일 업로드됨)')
            else:
                messages.success(request, '게시물이 작성되었습니다.')
            
            return redirect('post_detail', post_id=post.id)
            
        except Exception as e:
            messages.error(request, f'게시물 작성 중 오류: {str(e)}')
            print(f"게시물 작성 오류: {str(e)}")
    
    form = PostForm()
    return render(request, 'post_create.html', {'form': form, 'is_general': True})

def logout_view(request):
    """커스텀 로그아웃 뷰"""
    logout(request)
    messages.success(request, '안전하게 로그아웃되었습니다.')
    return redirect('login')

@login_required
def post_detail(request, post_id):
    """게시물 상세 페이지"""
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'post_detail.html', {'post': post})

