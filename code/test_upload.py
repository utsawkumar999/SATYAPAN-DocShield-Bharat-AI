import urllib.request

boundary = 'WebKitFormBoundary123456789'
body = (
    f'--{boundary}<r\n'
    'Content-Disposition: form-data; name="file"; filename="test.common.pdf"\r\n'
    'Content-Type: application/pdf\r\n\r\n'
    '%PDF-1.4 test content\r\n'
    f'--{boundary}--\r\n'
).encode('utf-8')

req = urllib.request.Request('http://localhost:8000/api/v1/omega/verify-omega', data=body, headers={
    'Content-Type': f'multipart/form-data; boundary={boundary}'
})

try:
    with urllib.request.urlopen(req) as resp:
        print('STATUS:', resp.status)
        print('RESPONSE:', resp.read().decode())
except Exception as e:
    print('ERROR:', e)
