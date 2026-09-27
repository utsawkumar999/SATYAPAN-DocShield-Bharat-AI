import urllib.request

boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
body = (
    f'--{boundary}\r\n'
    'Content-Disposition: form-data; name="file"; filename="aadhaar_card.pdf"\r\n'
    'Content-Type: application/pdf\r\n\r\n'
    'sample_pdf_binary_stream_data\r\n'
    f'--{boundary}--\r\n'
).encode('utf-8')

req = urllib.request.Request(
    'http://localhost:8000/api/v1/verify',
    data=body,
    headers={'Content-Type': f'multipart/form-data; boundary={boundary}'}
)

try:
    with urllib.request.urlopen(req) as resp:
        print('STATUS:', resp.status)
        print('RESPONSE:', resp.read().decode())
except Exception as e:
    print('ERROR:', e)
