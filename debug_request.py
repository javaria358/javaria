import urllib.request
import urllib.error
urls = [
    'http://127.0.0.1:8000/',
    'http://127.0.0.1:8000/admin-dashboard/',
]
for u in urls:
    try:
        with urllib.request.urlopen(u) as r:
            data = r.read()
            print(u, '=>', r.status, len(data))
    except urllib.error.HTTPError as e:
        print(u, 'HTTPError', e.code, e.reason)
        if e.fp is not None:
            body = e.fp.read().decode('utf-8', errors='ignore')
            print('BODY:', body[:1000])
    except Exception as e:
        print(u, 'ERROR', type(e).__name__, e)
