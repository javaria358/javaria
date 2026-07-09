import os
os.chdir(r'c:\Users\Admin\Desktop\djenfofinalproject')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_lms.settings')
import django
django.setup()
from django.urls import resolve, get_resolver
from django.conf import settings
print('DEBUG', settings.DEBUG)
print('ROOT_URLCONF', settings.ROOT_URLCONF)
resolver = get_resolver()
print('url patterns count:', len(resolver.url_patterns))
for p in resolver.url_patterns:
    print('pattern:', p.pattern, 'name:', getattr(p, 'name', None), 'callback:', getattr(p, 'callback', None))
try:
    match = resolve('/admin-dashboard/')
    print('resolved:', match.func, match.url_name, match.args, match.kwargs)
except Exception as e:
    print('resolve error:', type(e).__name__, e)
