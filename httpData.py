import struct
"""
Strip the header from http response
"""
def stripHeader(header):
    header = header.split(b"\r\n\r\n")
    header = header[1:]
    return b"".join(header)



"""
Strip metadata from chunked transfer encoding packets
"""
def getChunks(data:bytes):
    numbBytes = int(struct.unpack('>H', data[0:2])[0])
    print("NUMBER OF BYTES IN CHUNK: ", numbBytes)
    if data:
        numbBytes += 5
        data = data[5:numbBytes]
    return data

if __name__ == "__main__":
    f = open("index.html", "r")
    string = f.read()
    
    myString = stripHeader(string)
    
    print(myString)
    
   