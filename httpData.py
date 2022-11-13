
def stripHeader(header):
    header = header.split("\r\n")
    
    return header[1:]

def getChunks(data:list):
    pData = []
    for chunk in data:
        pData.append(chunk[2:-1])
    return pData