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
  
  
#TODO erase
def chksum(packet):
  if len(packet) % 2 != 0:
      packet += b'\0'    
  res = sum(array.array("H", packet))
  res = (res >> 16) + (res & 0xffff)
  res += res >> 16    
  return (~res) & 0xffff

 

if __name__ == "__main__":
  # Example checksum from: https://www.securitynik.com/2015/08/calculating-udp-checksum-with-taste-of_3.html
  ph = "110000001010100000000000000111111100000010101000000000000001111000000000000001100000000000010110"
  h = "00000000000101000000000000001010000000000000000000000000000010100000000000000000000000000000000001010000000000100010000000000000000000000000000000000000000000000100100001101001"
  tcp_checksum(ph, h)
  
