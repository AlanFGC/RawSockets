import array

def tcp_checksum_2(packet):
  # adds a byte if they are not equally diviseble by 2
  if len(packet) % 2 != 0:
      packet += b'\0'
  # standard sum
  res = sum(array.array("H", packet))
  # note that the following techniques were seen here:
  # https://medium.com/@NickKaramoff/tcp-packets-from-scratch-in-python-3a63f0cd59fe
  # https://www.bitforestinfo.com/blog/01/14/python-codes-to-calculate-tcp-checksum.html
  res = (res >> 16) + (res & 0xffff)
  res += res >> 16    
  return (~res) & 0xffff

 

if __name__ == "__main__":
  # Example checksum from: https://www.securitynik.com/2015/08/calculating-udp-checksum-with-taste-of_3.html
  pass
