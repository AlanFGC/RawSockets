def calculate_checksum(header):
    
    groups = []
    start = 0
    end = 16
    while end <= len(header):
        groups.append("0b" + header[start:end])
        start += 16
        end += 16
    
    total = 0

    for i in range(len(groups)):
        total += int(groups[i], 2)
    
    total = bin(total)[2:]

    diff = len(total) - 16
    
    if diff > 0:
        total = bin(int(total[:diff], 2) + int(total[diff:], 2))[2:]
    
    diff = 16 - len(total)
    total = "0" * diff + total

    out = ""

    for char in total:
        if char == "1":
            out += "0"
        else:
            out += "1"

    return out
        


if __name__ == "__main__":
    example2 = "0100010100000000000000000011010000101111011100000100000000000000010000000000011000000000000000001100000010101000010000000000011100100010011010111101110101010010"
    calculate_checksum(example2)