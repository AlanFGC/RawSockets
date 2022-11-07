from ast import Bytes
import socket
import random
import ip_checksum
import tcp_checksum
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

def make_ip_header(data:bytes, src: str, dest: str) -> bytes:
    
    a1 = struct.pack("!")
    # IPv4
    version = "0100"

    src = address_to_binary(src)
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

    # placeholder
    checksum = "0" * 16
    

    temp_head = version + ihl + type_of_service + total_length + identification + flag + fragment_offset + ttl + protocol + checksum + src + dest
    byte_checkSum = convert_Bit_String_to_bytes(ip_checksum.calculate_checksum_ip(temp_head))
    
    
    ip_header = convert_Bit_String_to_bytes(temp_head)
    byteArr = bytearray()
    appendByte(byteArr, ip_header, len(ip_header))
    appendByte(byteArr, data, len(data))
    header = byteArr[:10] + byte_checkSum + byteArr[12:]
    
    if len(header) != 20 + len(data):
        print("IP HEADER LEN:" , len(header))
        raise ValueError("Ip header incorrect Size")
    
    return header


def make_tcp_header_2(data:bytes, srcPort: int, destPort: int, seqNumb: int,
                    ackNumb: int, window: int, syn: bool, ack:bool, fin:bool, 
                    src_ip:str, dest_ip:str):
    # !HHIIBBHHH',
    a1 = struct.pack('!HH', srcPort, destPort)
    a2 = struct.pack('!II', seqNumb, ackNumb)
    a3 = struct.pack('!B', 5 << 4)
    syn = "1" if syn else "0"
    ack = "1" if ack else "0"
    fin = "1" if fin else "0"
    flags = "000" + ack + "00" + syn + fin
    a4 = struct.pack('!B', int(flags, 2))
    a5 = struct.pack('!H', int(window))
    a6 = struct.pack('!H', 0)
    a7 = struct.pack('!H', 0)
    packet = b''.join([a1,a2,a3,a4,a5,a6,a7])
    ip_header = struct.pack('!4s4sHH',socket.inet_aton(src_ip),socket.inet_aton(dest_ip),int("00000110",2),len(packet) + len(data))
    
    checksum = tcp_checksum.chksum(ip_header + packet)
    
    # checksum is not big endian
    packet = packet[:16] + struct.pack('H', checksum) + packet[18:]
    
    if len(packet) != 20:
        raise ValueError("WRONG SIZE FOR PACKET", len(packet))
    
    return packet + data

def make_tcp_header(data:bytes, srcPort: int, destPort: int, seqNumb: int,
                    ackNumb: int, window: int, syn: bool, ack:bool, fin:bool, 
                    src_ip:str, dest_ip:str):
    srcPort = "{0:b}".format(srcPort, '016b')
    srcPort = "0" * (16 - len(srcPort)) + srcPort
    destPort = "{0:b}".format(destPort, '016b')
    destPort = "0" * (16 - len(destPort)) + destPort
    # Sequence Number, Acknowledge Number
    seqNumb = "{0:b}".format(seqNumb, '016b')
    seqNumb = "0" * (32 - len(seqNumb)) + seqNumb
    ackNumb = "{0:b}".format(ackNumb, '016b')
    ackNumb = "0" * (32 - len(ackNumb)) + ackNumb
    # DO, RSV, FLAGS
    syn = "1" if syn else "0"
    ack = "1" if ack else "0"
    fin = "1" if fin else "0"
    headerSize = "01010000" # 8 bits
    flags = "000" + ack + "00" + syn + fin # 8 bits
    # window size
    window = "{0:b}".format(window, '016b')
    window = "0" * (16 - len(window)) + window
    # checksum and urgent
    checksum = "0" * 16
    extra = "0" * 16
    temp_head = str(srcPort) + str(destPort) + str(seqNumb) + str(ackNumb) + headerSize + flags + str(window) + checksum + extra
    
    tcp_length = decimal_to_binary(20 + len(data), 16)
    checksum = tcp_checksum.tcp_checksum(address_to_binary(src_ip), address_to_binary(dest_ip), "00000110", tcp_length, temp_head)
    temp_head = str(srcPort) + str(destPort) + str(seqNumb) + str(ackNumb) + headerSize + flags + str(window) + checksum + extra

    tcp_header = convert_Bit_String_to_bytes(temp_head)
    byteArr = bytearray()
    appendByte(byteArr, tcp_header, len(tcp_header))
    appendByte(byteArr, data, len(data))
    return bytes(byteArr)

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
    total_length = int(struct.unpack('>H', data[2:4])[0])
    # checksum as integer
    checkSum = int(struct.unpack('>H', data[8:10])[0])
    
    # ip data
    src = data[12:16]
    dest = data[16:20]
    src_ip = bytes_to_address(src)
    dest_ip = bytes_to_address(dest)
    print(f'src: {src_ip}')
    print(f'dest: {dest_ip}')
    print(f'Total Length: {total_length}')
    # the rest of the packet    
    raw_data = data[20:]
    return raw_data
    
"""
This function accepts data that's wrapped in an tcp header 
"""
def parse_TCP_packet(data: bytes):
    srcPort = int(struct.unpack('>H', data[0:2])[0])
    destPort = int(struct.unpack('>H', data[2:4])[0])
    seqNumber = int(struct.unpack('>I', data[4:8])[0])
    ackNumber = int(struct.unpack('>I', data[8:12])[0])
    window = int(struct.unpack('>H', data[14:16])[0])
    print(f'PORTS: SRC:{srcPort} dest:{destPort}')
    print(f'SqnceNumb: {seqNumber}')
    print(f'ackNumber: {ackNumber}')
    raw_data = data[20:]
    return srcPort, destPort, seqNumber, ackNumber, raw_data, window


if __name__ == "__main__":
    myBytes = bytes(b"hello World!")
    make_tcp_header(myBytes, 5004, 80, 321401244, 4213209102, 25, True, True, False)
