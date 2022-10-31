import socket
import sys
import random
import checksum_ip as cs

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
    version = "0100"

    source = "73.186.26.46"
    source = address_to_binary(source)

    dest = socket.gethostbyname(sys.argv[1])
    dest = address_to_binary(dest)

    type_of_service = "00100000"    # https://www.omnisecu.com/tcpip/ipv4-protocol-and-ipv4-header.php#:~:text=%22Type%20of%20Service%20(ToS),delay%2C%20throughput%2C%20and%20reliability.

    identification = random.randint(0, 2**16)
    identification = decimal_to_binary(identification, 16)

    flag = "000"
    fragment_offset = "0000000000000"

    ttl = "00010000"    # 32 hops should be enough, right?

    protocol = "00000110"   # 6 = TCP

    options = ""
    padding_len = 32 - len(options)
    padding = "0" * 32      

    ihl = 5  # compute after all variables initialized
    if padding:
        ihl += (len(padding) / 8) / 4
    total_length = ihl #+ len(data) / 8      # Assume no optional data

    ihl = decimal_to_binary(ihl, 4)
    total_length = decimal_to_binary(total_length, 16)

    checksum = "0000000000000000"

    temp_head = version + ihl + type_of_service + total_length + identification + flag + fragment_offset + ttl + protocol + checksum + source + dest
    checksum = cs.calculate_checksum(temp_head)

if __name__ == "__main__":
    make_ip_header("11111111")
    print("0" * 0)
    print("0" * 1)
    print("0" * 2)