
example = "0100010100000000000000000011110000011100010001100100000000000000010000000000011000000000000000001010110000010000000010100110001110101100000100000000101000001100"

def add_binary(bin1, bin2):

    dec1 = int(bin1, 2)
    dec2 = int(bin2, 2)

    total = dec1 + dec2
    total = bin(total)
    total = total[2:]
    chunk_size = 16

    # size_difference = chunk_size - total(len)
    # if size_difference < 0:
    #     prepend = ""
    #     while size_difference < 0:
    #         prepend += "0"
    #         size_difference += 1
    #     total = "0b" + prepend + total
    # elif size_difference > 0:
    #     pass



    print(bin1)
    print(bin2)
    print(total)

def calculate_checksum(header):
    '''
    Checksum only applies to the first 5 lines of the header.
    '''
    groups = []
    start = 0
    end = 16
    while end <= len(header):
        groups.append("0b" + header[start:end])
        start += 16
        end += 16
    print(groups)
    
    # total = 0
    # for i in groups:
    #     add_binary()
    
    # checksum = bin(total).replace("0b", "")
    # print(checksum)
    # print(len(checksum))

    add_binary('0b1010110000010000', '0b1010110000010000')
    print(" ")
    add_binary('0b0000000000111100', '0b0000101000001100')
        


if __name__ == "__main__":
    calculate_checksum(example)