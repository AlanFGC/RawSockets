import random
import tcp_checksum as cs

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

def create_tcp_header(source_port, data, source_ip, dest_ip):

# 0                   1                   2                   3
# 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |          Source Port          |       Destination Port        |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                        Sequence Number                        |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                    Acknowledgment Number                      |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |  Data |           |U|A|P|R|S|F|                               |
# | Offset| Reserved  |R|C|S|S|Y|I|            Window             |
# |       |           |G|K|H|T|N|N|                               |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |           Checksum            |         Urgent Pointer        |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                    Options                    |    Padding    |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                             data                              |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

    source_port = decimal_to_binary(source_port, 16)

    dest_port = 80
    dest_port = decimal_to_binary(dest_port, 16)

    seq_number = random.randint(0, 2**32)
    seq_number = decimal_to_binary(seq_number, 32)

    ack_number = "0" * 32
    reserved = "0" * 6
    control_flag = "000010"

    # Window size starts at 1 for slow start algorithm
    window = "0000000000000001"

    checksum, urgent_pointer = "0" * 16

    data_offset = "0101"

    temp_header = source_port + dest_port + seq_number + ack_number + data_offset + reserved + control_flag + window + checksum + urgent_pointer
    pseudo_header = source_ip + dest_ip + "00000000" + "00000110" + decimal_to_binary(20, 16)   # TCP header contains no data

    checksum = cs.tcp_checksum(pseudo_header, temp_header)
    header = source_port + dest_port + seq_number + ack_number + data_offset + reserved + control_flag + window + checksum + urgent_pointer
    return header