from django import forms
from .models import Post, Announcement, PostFile
from django.contrib.auth.models import User
from .widgets import MultipleFileField

class PostForm(forms.ModelForm):
    # 커스텀 여러 파일 업로드 필드
    files = MultipleFileField(
        required=False,
        help_text='여러 파일을 선택하려면 Ctrl(Cmd) + 클릭하세요. 모든 파일 타입 지원!'
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full bg-black border border-gray-600 text-white p-2 text-sm',
                'placeholder': '제목을 입력하세요...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full bg-black border border-gray-600 text-white p-2 text-sm',
                'placeholder': '내용을 입력하세요... (파이썬 코드, 스크립트 등 자유롭게 작성)',
                'rows': 20
            }),
            'category': forms.Select(attrs={
                'class': 'w-full bg-black border border-gray-600 text-white p-2 text-sm'
            }),
        }

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full bg-black border border-gray-600 text-white p-2 text-sm',
                'placeholder': '공지 제목을 입력하세요...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full bg-black border border-gray-600 text-white p-2 text-sm',
                'placeholder': '공지 내용을 입력하세요...',
                'rows': 8
            })
        }

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'input-field w-full p-3 rounded font-mono',
        'placeholder': 'Enter secure passphrase...'
    }))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'input-field w-full p-3 rounded font-mono',
                'placeholder': 'Enter unique identifier...'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'input-field w-full p-3 rounded font-mono',
                'placeholder': 'secure.contact@domain.onion'
            })
        }

