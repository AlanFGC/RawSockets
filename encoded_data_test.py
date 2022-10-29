import random
import main

"""
This is a test that reads a file and splits it into a html file.
The goal of this test is to ensure that the files are joined together
correctly.
"""
def openHtml(fileName) -> list:
    with open(fileName, encoding = 'utf-8') as f:
        data = []
        tmp = f.read(1500)
        ptr = 0
        while tmp:
            data.append(tmp.encode())
            ptr += 1500
            f.seek(ptr)
            tmp = f.read(1500)
    return data

def makeArray(data):
    sqnce = random.randint(0, 4294967200 - len(data))
    dataArray = []
    for i in range(len(data)):
        dataArray.append((sqnce, data[i]))
        sqnce += 1
    return dataArray


def testJoiningData(fileName="linkedin.html"):    
    data = openHtml(fileName)
    array = makeArray(data)
    random.shuffle(array)
    main.joinData(array)
    
    return

"""
Main drive of the program
"""
if __name__ == "__main__":
    testJoiningData()