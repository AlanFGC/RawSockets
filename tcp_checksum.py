import ip_handler
def tcp_checksum(dataLen):
  checksum = "{0:b}".format(dataLen + 40, '016b')
  checksum = "0" * (16 - len(checksum)) + checksum
  print(checksum)
  return checksum
  
  

 

if __name__ == "__main__":
  # Example checksum from: https://www.securitynik.com/2015/08/calculating-udp-checksum-with-taste-of_3.html
  ph = "110000001010100000000000000111111100000010101000000000000001111000000000000001100000000000010110"
  h = "00000000000101000000000000001010000000000000000000000000000010100000000000000000000000000000000001010000000000100010000000000000000000000000000000000000000000000100100001101001"
  tcp_checksum(ph, h)
  
