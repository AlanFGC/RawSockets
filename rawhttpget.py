import imp
import socket
import sys
from subprocess import check_output

def main():
    
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
    # sock_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock_rec = socket.socket(socket.SOCK_RAW, socket.IPPROTO_TCP)

    # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # s.connect(("8.8.8.8", 80))
    # print(s)

    # https://stackoverflow.com/questions/24196932/how-can-i-get-the-ip-address-from-a-nic-network-interface-controller-in-python
    ips = check_output(['hostname', '--all-ip-addresses'])
    print(ips)

    # message = "Hello world".encode()
    # sock_send.sendall(message)

if __name__ == "__main__":
    main()