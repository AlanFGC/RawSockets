
import ip_handler
import socket

"""
Evan Hanes
Alan Garcia
19 october 2022
"""
  
"""
Not quite sure
"""
def rawSock():
    con = socket(AF_INET, SOCK_RAW, IPPROTO_TCP)
    
  
  
 """
 Join data stored in a sorted array with the following format: (sequence number, data in bytes)
 """
def joinData(array) -> string:
    data = sorted(array, key=lambda key:array[0])
    string = ""
    for item in data:
        string += str(item[1], "ascii")
    return string

rawSock()


