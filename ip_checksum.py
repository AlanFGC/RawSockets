"""
This function add two binary numbers
"""
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

"""
This is an IP checkSum, takes the header
"""
def calculate_checksum_ip(header):
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
    return checksum
        
