import array

def tcp_checksum(source_ip, dest_ip, protocol, tcp_length, tcp_header):
  # Pseudo-header = source_ip + dest_ip + reserved + protocol + TCP_length
  pseudo_header = source_ip + dest_ip + "00000000" + protocol + tcp_length

  start = 0
  end = 16

  chunks = []

  while end <= len(pseudo_header):
    chunks.append(pseudo_header[start:end])
    start += 16
    end += 16
  
  start = 0
  end = 16



  while end <= len(tcp_header):
    chunks.append(tcp_header[start:end])
    start += 16
    end += 16
  
  for i in range(len(chunks)):
    chunks[i] = int(chunks[i], 2)
  
  total = sum(chunks)
  checksum = bin(total)[2:]

  diff = len(checksum) - 16
  if diff > 0:
    carry_over = checksum[:diff]
    checksum = checksum[diff:]
    checksum = bin(int(checksum, 2) + int(carry_over, 2))[2:]
    
  diff = 16 - len(checksum)
  if diff > 0:
    prepend = "0" * diff
    checksum = prepend + checksum

  out = ""
  for i in range(16):
    if checksum[i] == "0":
      out += "1"
    else:
      out += "0"

  return out


def calculate_checksum_tcp(init_packet):
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
  

def tcp_checksum_2(packet):
  if len(packet) % 2 != 0:
      packet += b'\0'
  # note that these techniques were used by observing scapy and other codebases
  # they were used here:
  # https://www.bitforestinfo.com/blog/01/14/python-codes-to-calculate-tcp-checksum.html
  # https://medium.com/@NickKaramoff/tcp-packets-from-scratch-in-python-3a63f0cd59fe
  res = sum(array.array("H", packet)) # this is the actual summation of all the elements
  res = (res >> 16) # bitshift 16
  res += (res & 0xffff) # and operation address overflow
  res += res >> 16   # perform it again
  return (~res) & 0xffff # and operation again


 

if __name__ == "__main__":
  # Example checksum from: https://www.securitynik.com/2015/08/calculating-udp-checksum-with-taste-of_3.html
  pass