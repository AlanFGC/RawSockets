import socket
import ip_handler

def main():

    example = "010001010000000000000000001111001010110100001000010000000000000001000000000001100000000010011011110000001010100001000000000001111100110000101100110000000011110010011111101011000000000001010000001100100011010001010100110011100000000000000000000000000000000010100000000000101111101011110000011001111110110100000000000000000000001000000100000001011011010000000100000000100000100000001010111000001110001101010000001001100000000000000000000000000000000000000001000000110000001100000111"

    dest = socket.gethostbyname("david.choffnes.com")

    # Create two ephemeral sockets to get their ports
    eff_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    eff_socket.sendto(b"HI", ('127.0.0.1', 80))
    port_send = eff_socket.getsockname()[1]

    eff_socket_2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    eff_socket_2.sendto(b"HI", ('127.0.0.1', 80))
    port_rec = eff_socket_2.getsockname()[1]

    eff_socket.close()      # Close ephemeral sockets
    eff_socket_2.close()

    # Create epemeral socket to get IP address
    # NOTE: socket.gethostbyname(socket.gethostname()) returns localhost on
    # Ubuntu 22.04
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()

    # Create one socket for sending data, another for receiving data
    sock_send = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    sock_rec = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

    packet = ip_handler.make_ip_header(ip_handler.make_tcp_header(b"", port_send, port_rec, 1234, 2345, 1, True, False, False), local_ip, dest)

    # Set socket options and bind them to their respective ports
    sock_send.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    sock_send.bind((local_ip, port_send))
    send = sock_send.sendto(packet, (dest, 80))
    
    sock_rec.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    sock_rec.bind((local_ip, port_rec))
    rec = sock_rec.recv(1500)
    for i in range(10):
        rec += sock_rec.recv(1500)
    print(rec)
    ip_handler.parse_TCP_packet(ip_handler.parse_IP_packet(rec))


if __name__ == "__main__":
    main()