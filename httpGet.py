"""
Get request
"""
def craftRequest(url: str, subdomain: str) -> bytes:
    request = "GET /" + subdomain + " HTTP/1.1\r\n" + "Host: " + url + "\r\n"
    content = "Content-Length: 0\r\n"
    request = request + content + "\r\n"

    return request.encode("ascii")