 
example = "0100010100000000000000000011110000011100010001100100000000000000010000000000011000000000000000001010110000010000000010100110001110101100000100000000101000001100"

def add_binary(bin1, bin2):

    dec1 = int(bin1, 2)
    dec2 = int(bin2, 2)
    total = dec1 + dec2
    total = bin(total)
    if len(total) < len(bin1):
        prepend = "0" * (len(bin1) - len(total))
        total = "0b" + prepend + total[2:]
    if len(total) > len(bin1):
        keep = "0b" + total[3:]
        keep = int(keep, 2) + 1
        total = bin(keep)[2:]
        prepend = "0" * (16 - len(total))
        total = "0b" + prepend + total

    return total

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
    
    checksum = groups[0]
    for i in range(1, len(groups)):
        checksum = add_binary(checksum, groups[i])
    
    checksum = checksum.replace("0b", "")
    print(checksum)
    print(len(checksum))
        


if __name__ == "__main__":
    calculate_checksum(example)