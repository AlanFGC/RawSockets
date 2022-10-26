import socket
import sys

def decimal_to_binary(address: str):
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
    


def main():

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
    dest = decimal_to_binary(dest)

    ihl = None  # computer after all variables initialized
    

if __name__ == "__main__":
    main()