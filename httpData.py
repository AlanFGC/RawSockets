
def stripHeader(header):
    header = header.split(b"\r\n\r\n")
    header = header[1:]
    return b"".join(header)

def getChunks(data:list):
    chunks = []
    
    for chunk in data:
        chunk = chunk.split(b"\r\n")
        if chunk:
            chunk = chunk[1:]
        chunks.append(b"".join(chunk))
    
    return chunks

if __name__ == "__main__":
    f = open("index.html", "r")
    string = f.read()
    
    myString = stripHeader(string)
    
    print(myString)
    
   