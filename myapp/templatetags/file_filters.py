from django import template
import os

register = template.Library()

@register.filter
def is_image(file_obj):
    """PostFile 객체가 이미지인지 확인하는 필터"""
    if not file_obj or not hasattr(file_obj, 'file'):
        return False
    
    try:
        file_url = file_obj.file.url
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.ico', '.tiff', '.tif']
        file_extension = os.path.splitext(file_url.lower())[1]
        return file_extension in image_extensions
    except:
        return False

@register.filter
def is_video(file_obj):
    """PostFile 객체가 동영상인지 확인하는 필터"""
    if not file_obj or not hasattr(file_obj, 'file'):
        return False
    
    try:
        file_url = file_obj.file.url
        video_extensions = ['.mp4', '.avi', '.mov', '.webm', '.mkv', '.flv', '.wmv', '.m4v', '.3gp', '.ogv']
        file_extension = os.path.splitext(file_url.lower())[1]
        return file_extension in video_extensions
    except:
        return False

@register.filter
def get_filename(file_obj):
    """PostFile 객체에서 파일명 추출"""
    if not file_obj:
        return ""
    
    if hasattr(file_obj, 'original_name'):
        return file_obj.original_name
    elif hasattr(file_obj, 'file'):
        return os.path.basename(file_obj.file.name)
    else:
        return str(file_obj)

@register.filter
def get_file_extension(file_obj):
    """PostFile 객체에서 파일 확장자 추출"""
    if not file_obj or not hasattr(file_obj, 'file'):
        return ""
    
    try:
        return os.path.splitext(file_obj.file.name.lower())[1]
    except:
        return ""

@register.filter
def get_file_type(file_obj):
    """PostFile 객체의 파일 타입 분류"""
    if not file_obj:
        return "unknown"
    
    if hasattr(file_obj, 'get_file_type'):
        return file_obj.get_file_type()
    
    try:
        ext = os.path.splitext(file_obj.file.name.lower())[1]
        
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
    except:
        return "unknown"

@register.filter
def get_file_size(file_obj):
    """PostFile 객체의 파일 크기 반환 (바이트)"""
    if not file_obj:
        return 0
    
    if hasattr(file_obj, 'get_file_size'):
        return file_obj.get_file_size()
    
    try:
        return file_obj.file.size
    except:
        return 0

@register.filter
def format_file_size(size_bytes):
    """파일 크기를 읽기 쉬운 형태로 변환"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

@register.filter
def get_file_icon(file_type):
    """파일 타입에 따른 아이콘 반환"""
    icons = {
        'image': '🖼️',
        'video': '🎬',
        'audio': '🎵',
        'pdf': '📄',
        'text': '📝',
        'document': '📄',
        'spreadsheet': '📊',
        'presentation': '📽️',
        'archive': '📦',
        'executable': '⚙️',
        'code': '💻',
        'file': '📎'
    }
    return icons.get(file_type, '📎')
