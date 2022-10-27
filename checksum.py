
def calculate_checksum(header):
    '''
    Checksum only applies to the first 5 lines of the header.
    '''
    groups = []
    start = 0
    end = 16
    while end <= len(header):
        groups.append((header[start:end], start, end))
        start += 16
        end += 16
    
    print(header)
    print(len(header))
    print(groups)


if __name__ == "__main__":
    calculate_checksum(None)