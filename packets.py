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
    print(type(data))
    length = b"\x00\x00" + bytes(len(bytes))
    print(length)
    packet = bytearray()
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

packIP('192.168.1.232', '123.213.32.100', bytes(random.getrandbits(11200)))