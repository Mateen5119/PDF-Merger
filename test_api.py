import urllib.request
import urllib.parse
import json
import os
import mimetypes

# Multipart form-data encoder without requests library
def encode_multipart_formdata(fields, files):
    boundary = "----------Boundary12345"
    body = bytearray()

    for key, value in fields.items():
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode())
        body.extend(f"{value}\r\n".encode())

    for key, filename, value in files:
        mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(f'Content-Disposition: form-data; name="{key}"; filename="{filename}"\r\n'.encode())
        body.extend(f'Content-Type: {mimetype}\r\n\r\n'.encode())
        body.extend(value)
        body.extend(b"\r\n")

    body.extend(f"--{boundary}--\r\n".encode())
    return body, f"multipart/form-data; boundary={boundary}"

def test_upload():
    print("Testing /merge_PDFs endpoint...")
    
    with open(r'x:\PDF-Merger\test1.pdf', 'rb') as f1, open(r'x:\PDF-Merger\test2.pdf', 'rb') as f2:
        files = [
            ('pdfs', 'test1.pdf', f1.read()),
            ('pdfs', 'test2.pdf', f2.read())
        ]
        
    body, content_type = encode_multipart_formdata({}, files)
    
    req = urllib.request.Request("http://127.0.0.1:5000/merge_PDFs", data=body, headers={'Content-Type': content_type})
    try:
        response = urllib.request.urlopen(req)
        if response.status == 200:
            with open(r'x:\PDF-Merger\merged_test.pdf', 'wb') as f:
                f.write(response.read())
            print("Success! Merged PDF saved to disk.")
        else:
            print(f"Failed with status: {response.status}")
    except Exception as e:
        print(f"Error connecting: {e}")

if __name__ == '__main__':
    test_upload()
