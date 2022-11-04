import array

def create_tcp_checksum(init_packet):

    if len(init_packet) % 2 != 0:
        init_packet += b'\0'
    
    total = sum(array.array("H", init_packet))

    num_bits = total.bit_length()

    difference = 0
    if len(num_bits) > 16:
        difference = len(total) - 16
    
    overflow = total >> 16
    main = total << difference

    total = overflow + main

    return ~total
