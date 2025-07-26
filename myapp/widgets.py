from django import forms
from django.forms.widgets import Widget
from django.utils.html import format_html
from django.utils.safestring import mark_safe

class MultipleFileInput(Widget):
    """여러 파일 업로드를 지원하는 커스텀 위젯"""
    
    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        super().__init__(attrs)
    
    def render(self, name, value, attrs=None, renderer=None):
        """HTML input[type=file] 태그를 직접 렌더링"""
        if attrs is None:
            attrs = {}
        
        # 기본 CSS 클래스 설정
        css_class = attrs.get('class', 'w-full bg-black border border-gray-600 text-white p-2 text-sm')
        
        # HTML 직접 생성
        html = f'<input type="file" name="{name}" multiple class="{css_class}" />'
        
        return mark_safe(html)
    
    def value_from_datadict(self, data, files, name):
        """여러 파일을 처리하도록 오버라이드"""
        if hasattr(files, 'getlist'):
            return files.getlist(name)
        else:
            file_list = files.get(name)
            return [file_list] if file_list else []

class MultipleFileField(forms.Field):
    """여러 파일을 처리하는 커스텀 필드"""
    
    widget = MultipleFileInput
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)
    
    def clean(self, data):
        """파일 데이터 검증"""
        if not data:
            if self.required:
                raise forms.ValidationError("파일을 선택해주세요.")
            return []
        
        # 단일 파일인 경우 리스트로 변환
        if not isinstance(data, list):
            data = [data] if data else []
        
        # 빈 파일 제거
        files = [f for f in data if f and hasattr(f, 'name')]
        
        # 파일 크기 검증 (각 파일당 500MB 제한)
        max_size = 500 * 1024 * 1024  # 500MB
        for file in files:
            if hasattr(file, 'size') and file.size > max_size:
                raise forms.ValidationError(f"파일 '{file.name}'이 너무 큽니다. (최대 500MB)")
        
        return files

