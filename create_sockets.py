import socket
import ip_handler as ip

def main():

    our_data = ip.make_ip_header("hi").encode()

    example = "010001010000000000000000001111001010110100001000010000000000000001000000000001100000000010011011110000001010100001000000000001111100110000101100110000000011110010011111101011000000000001010000001100100011010001010100110011100000000000000000000000000000000010100000000000101111101011110000011001111110110100000000000000000000001000000100000001011011010000000100000000100000100000001010111000001110001101010000001001100000000000000000000000000000000000000001000000110000001100000111"

    dest = socket.gethostbyname("david.choffnes.com")

    eff_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    eff_socket.sendto(b"HI", ('127.0.0.1', 80))
    port_send = eff_socket.getsockname()[1]

    eff_socket_2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    eff_socket_2.sendto(b"HI", ('127.0.0.1', 80))
    port_rec = eff_socket_2.getsockname()[1]

    eff_socket.close()
    eff_socket_2.close()

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()

    sock_send = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    sock_rec = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

    sock_send.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    sock_send.bind((local_ip, port_send))
    send = sock_send.sendto(our_data, (dest, 80))
    
    print(send)
    sock_rec.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    sock_rec.bind((local_ip, port_rec))
    rec = sock_rec.recv(1500)
    return rec
    print(rec)


if __name__ == "__main__":
    print(ip.parse_IP_packet(main()))