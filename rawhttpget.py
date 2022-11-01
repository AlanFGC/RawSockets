import socket
import sys
from subprocess import check_output

def main(packet):

    example = b"010001010000000000000000001111001010110100001000010000000000000001000000000001100000000010011011110000001010100001000000000001111100110000101100110000000011110010011111101011000000000001010000001100100011010001010100110011100000000000000000000000000000000010100000000000101111101011110000011001111110110100000000000000000000001000000100000001011011010000000100000000100000100000001010111000001110001101010000001001100000000000000000000000000000000000000001000000110000001100000111"
    
    #s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    sock_send = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    sock_rec = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    #sock_send.sendall(packet)

    # https://stackoverflow.com/questions/24196932/how-can-i-get-the-ip-address-from-a-nic-network-interface-controller-in-python
    ips = check_output(['hostname', '--all-ip-addresses']).decode()
    sender = ips.split(" ")[0]

    dest = socket.gethostbyname("david.choffnes.com")
    print(dest)
    print(sock_send.sendto(example, (dest, 80)))

    # message = "Hello world".encode()
    # sock_send.sendall(message)

if __name__ == "__main__":
    main(None)