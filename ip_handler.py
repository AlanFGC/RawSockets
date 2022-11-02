from audioop import add
from operator import le
import socket
import random
from tokenize import String
import checksum_ip as cs
import struct

"""
This mini library is made to handle IP packets
"""


def bytes_to_address(source: bytes):
    arr = []
    for i in range(len(source)):
        arr.append(str(int(source[i])))
        
    return ".".join(arr)


def address_to_binary(address: str):
    '''
    Takes an IP address in decimal notation as a string
    and returns the same IP address in binary.
    '''

    address = address.split(".")
    out = ""
    for i in address:

        bits = []
        i = int(i)
        while i:
            bits.append(i % 2)
            i = i // 2

        missing = 8 - len(bits)
        while missing:
            bits.append(0)
            missing -= 1

        bits.reverse()

        for bit in bits:
            out += str(bit)

    return out
    

def decimal_to_binary(value, num_digits):

    bits = []
    while value:
        bits.append(value % 2)
        value = value // 2

    missing = num_digits - len(bits)
    while missing:
        bits.append(0)
        missing -= 1
    
    bits.reverse()
    
    out = ""
    for i in bits:
        out += str(i)
    
    return out


# 0                   1                   2                   3
# 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |Version|  IHL  |Type of Service|          Total Length         |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |         Identification        |Flags|      Fragment Offset    |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |  Time to Live |    Protocol   |         Header Checksum       |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                       Source Address                          |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                    Destination Address                        |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                    Options                    |    Padding    |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


def make_ip_header(data):
    # Construct IP header
    hostname = socket.gethostname()
   
    IP = socket.gethostbyname(hostname)
    
    # IPv4
    version = "0100"

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    source = s.getsockname()[0]
    s.close()
    source = address_to_binary(source)

    dest = socket.gethostbyname("www.google.com")
    
    dest = address_to_binary(dest)
    
    

    type_of_service = "00100000"    # https://www.omnisecu.com/tcpip/ipv4-protocol-and-ipv4-header.php#:~:text=%22Type%20of%20Service%20(ToS),delay%2C%20throughput%2C%20and%20reliability.

    identification = random.randint(0, 2**16)
    identification = decimal_to_binary(identification, 16)

    flag = "010"
    fragment_offset = "0000000000000"

    ttl = "00100000"    # 32 hops should be enough, right?

    protocol = "00000110"   # 6 = TCP

    ihl = "0101"
    total_length = 20 + len(data)
    total_length = "{0:b}".format(total_length, '016b')
    total_length = "0" * (16 - len(total_length)) + total_length
    
    
    
    if len(ihl) != 4 or len(total_length) != 16:
        raise ValueError("Incorrect IHL or Total_Length size")

    # checksum set to disabled
    checksum = "1111110001011010"
    

    temp_head = version + ihl + type_of_service + total_length + identification + flag + fragment_offset + ttl + protocol + checksum + source + dest
    checksum = cs.calculate_checksum(temp_head)
    if len(temp_head) != 160:
        print("IP HEADER LEN:" + len(temp_head))
        raise ValueError("Ip header incorrect Size")
    ip_header = version + ihl + type_of_service + total_length + identification + flag + fragment_offset + ttl + protocol + checksum + source + dest + data
    return ip_header
    # ip_header = convert_Bit_String_to_bytes(temp_head)
    # byteArr = bytearray()
    # appendByte(byteArr, ip_header, len(ip_header))
    # appendByte(byteArr, data, len(data))
    
    # return bytes(byteArr)

def appendByte(array, bytes, size):
    for i in range(size):
        array.append(bytes[i])
    return


def convert_Bit_String_to_bytes(s):
    return int(s, 2).to_bytes((len(s) + 7) //8, byteorder='big')


"""
This function accepts data that's wrapped in an IP header
"""
def parse_IP_packet(data: bytes):
    # version as string
    version = bin(int(str(data[0]), base=16))[:2]
    # ihl as string
    ihl = bin(int(str(data[0]), base=16))[2:]
    # length as integer
    total_length = int(struct.unpack('>h', data[2:4])[0])
    # checksum as integer
    checkSum = int(struct.unpack('>h', data[8:10])[0])
    
    # ip data
    src = data[12:16]
    dest = data[16:20]
    src_ip = bytes_to_address(src)
    dest_ip = bytes_to_address(dest)
    
    # the rest of the packet    
    raw_data = data[20:]
    return version, ihl, total_length, checkSum, src_ip, dest_ip, raw_data
    
"""
This function accepts data that's wrapped in an tcp header 
"""
def parse_TCP_packet(data: bytes):
    srcPort = int(struct.unpack('>h', data[0:2])[0])
    destPort = int(struct.unpack('>h', data[2:4])[0])
    seqNumber = int(struct.unpack('>h', data[4:8])[0])
    ackNumber = int(struct.unpack('>h', data[8:12])[0])
    raw_data = data[20:]
    return srcPort, destPort, seqNumber, ackNumber, raw_data


if __name__ == "__main__":
    myBytes = make_ip_header(bytes(b"hello World!"))
    print(myBytes)
    print(len(myBytes))
    out = parse_IP_packet(myBytes)
    print(out)
