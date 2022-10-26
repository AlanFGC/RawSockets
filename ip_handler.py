import socket
import sys
import random

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
        print(bits)

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


def make_ip_header(data):

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


    # Construct IP header
    hostname = socket.gethostname()
    IP = socket.gethostbyname(hostname)

    # IPv4
    version = "0010"

    dest = socket.gethostbyname(sys.argv[1])
    dest = address_to_binary(dest)

    type_of_service = "00100000"    # https://www.omnisecu.com/tcpip/ipv4-protocol-and-ipv4-header.php#:~:text=%22Type%20of%20Service%20(ToS),delay%2C%20throughput%2C%20and%20reliability.

    identifier = random.randint(0, 2**16)
    identifer = decimal_to_binary(identifer, 16)

    flag = "000"
    fragment_offset = "0000000000000"

    ttl = "00010000"    # 32 hops should be enough, right?

    protocol = "00000110"   # 6 = TCP

    ihl = None  # compute after all variables initialized

    total_length = ihl + len(data) / 8



    check_sum = "00000000"


if __name__ == "__main__":
    make_ip_header("11111111")