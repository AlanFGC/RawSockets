#!/usr/bin/env python3
"""
This set of functions will 
keep create packets that used to send
data through the web.
"""

from ctypes import sizeof
import socket
import random
from struct import pack

"""
This function will pack data into an IPV4 header. 
"""
def packIP(src, dest, data: bytes)->None:
    # this is a byte array, it can only append bytes that are less than 255, if you have a larger 'value' it won't work
    packet = bytearray()
    
    
    # you can get the length of the byte data just by performing this. 
    lenData = len(data)
    
    # this is how to convert integer into a mf byte of n size
    length = lenData.to_bytes(2, 'big')
    
    
    service = b'\x00\x00'
    srcB = socket.inet_aton(src)
    destB = socket.inet_aton(dest)
    packet.append(4)
    appendByte(packet, srcB, 4)
    print(srcB)
    print(packet)



def appendByte(array, bytes, size):
    for i in range(size):
        array.append(bytes[i])
    return

def byteFormat(myBytes, desiredSize):
    pass

packIP('192.168.1.232', '123.213.32.100', b'dajsddlajksdpasdkapdkaspd')