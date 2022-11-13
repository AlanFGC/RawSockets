
def stripHeader(header):
    header = header.split(b"\r\n\r\n")
    header = header[1:]
    return b"".join(header)

def getChunks(data:list):
    pData = []
    for chunk in data:
        pData.append(chunk[2:-1])
    return pData


if __name__ == "__main__":
    f = open("index.html", "r")
    string = f.read()
    
    myString = stripHeader(string)
    
    print(myString)
    
   