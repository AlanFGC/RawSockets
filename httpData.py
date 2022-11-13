def getChunks(data:list):
    pData = []
    for chunk in data:
        pData.append(chunk[-3])
    return pData