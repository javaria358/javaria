import os
os.chdir(r'c:\Users\Admin\Desktop\djenfofinalproject')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_lms.settings')
import django
django.setup()
from django.test import Client
c = Client()
for path in ['/', '/admin-dashboard/']:
    resp = c.get(path)
    print(path, resp.status_code, resp.url)
    print('headers', resp.items())
    if resp.status_code >= 300 and resp.status_code < 400:
        print('redirect to', resp['Location'])
    print('body length', len(resp.content))
    print('body snippet', resp.content[:300])
