import array
import struct

def create_tcp_checksum(init_packet):

    if len(init_packet) % 2 != 0:
        init_packet += b'\0'
    
    total = sum(array.array("H", init_packet))

    num_bits = total.bit_length()

    difference = 0
    if num_bits > 16:
        difference = len(total) - 16
    
    overflow = total >> 16
    main = total << difference

    total = overflow + main

    return ~total

if __name__ == "__main__":

    class TCPPacket:
        def __init__(self,
                    src_host,
                    src_port,
                    dst_host,
                    dst_port,
                    flags=0):
            self.src_host = src_host
            self.src_port = src_port
            self.dst_host = dst_host
            self.dst_port = dst_port
            self.flags = flags
        
        def build(self):
            packet = struct.pack(
                '!HHIIBBHHH',
                self.src_port,  # Source Port
                self.dst_port,  # Destination Port
                0,              # Sequence Number
                0,              # Acknoledgement Number
                5 << 4,         # Data Offset
                self.flags,     # Flags
                8192,           # Window
                0,              # Checksum (initial value)
                0               # Urgent pointer
            )
            return packet

    pack = TCPPacket(19945, 5, 338586, 997, 3)
    pack = pack.build()

    bleh = create_tcp_checksum(pack)
    print(bleh)

    
