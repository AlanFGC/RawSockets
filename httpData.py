import html
import re

"""
Strip the header from http response
"""
def stripHeader(header:bytes):
    header = header.split(b"\r\n\r\n")
    header = header[1:]
    return b"".join(header)



"""
Strip metadata from chunked transfer encoding packets
"""
def getChunkedData(data):
    data = "".join(data)
    list = re.findall("\n[0-9abcdf]+\n", data)
    for item in list:
        data = data.replace(item, "")
    return data


if __name__ == "__main__":
    pass