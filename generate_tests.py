import base64

b64 = "JVBERi0xLjEKJcKlwrHDqwoxIDAgb2JqCjw8IC9UeXBlIC9DYXRhbG9nIC9QYWdlcyAyIDAgUiA+PgplbmRvYmoKMiAwIG9iago8PCAvVHlwZSAvUGFnZXMgL0tpZHMgWzMgMCBSXSAvQ291bnQgMSA+PgplbmRvYmoKMyAwIG9iago8PCAvVHlwZSAvUGFnZSAvUGFyZW50IDIgMCBSIC9NZWRpYUJveCBbMCAwIDYxMiA3OTJdID4+CmVuZG9iagoKWFJFRgowIDQKMDAwMDAwMDAwMCA2NTUzNSBmCjAwMDAwMDAwMTggMDAwMDAgbgowMDAwMDAwMDc1IDAwMDAwIG4KMDAwMDAwMDEzMiAwMDAwMCBuClRSQUlMRVIKPDwgL1Jvb3QgMSAwIFIgL1NpemUgNCA+PgpzdGFydHhyZWYKMjE0CiUlRU9GCg=="

data = base64.b64decode(b64)

with open(r'x:\PDF-Merger\test1.pdf', 'wb') as f:
    f.write(data)

with open(r'x:\PDF-Merger\test2.pdf', 'wb') as f:
    f.write(data)

print("Generated test1.pdf and test2.pdf")
