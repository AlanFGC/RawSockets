import create_sockets as my_socks
import socket
import ip_handler

"""
Evan Hanes
Alan Garcia
19 october 2022
"""


def main(domain: str):
    domain = "david.choffnes.com"
    ext_dest_port = 80
    local_ip = my_socks.getLocalIp();
    
    rec_port, send_port = my_socks.getConnectionPorts(domain)
    dest_ip = socket.gethostbyname(domain)
    
    
    
    print(f'Local ip {local_ip}:{send_port}, destination ip {dest_ip }:{rec_port}')

    sock_send = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    sock_rec = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    
    packet = ip_handler.make_tcp_header_2(b"DATA", send_port, ext_dest_port, 666, 1, 1, True, False, False, local_ip, dest_ip)
    
    ip_handler.make_ip_header(packet, local_ip, dest_ip)
    
    
    
   
    # Set socket options and bind them to their respective ports
    sock_send.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    sock_send.bind((local_ip, send_port))
    
    sock_rec.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    sock_rec.bind((local_ip, rec_port))
    
    
    send = sock_send.sendto(packet, (dest_ip, ext_dest_port))
    
    rec = sock_rec.recv(1500)
    ip_handler.parse_TCP_packet(ip_handler.parse_IP_packet(rec))
    
    for i in range(10):
        rec = sock_rec.recv(1500)
        ip_handler.parse_TCP_packet(ip_handler.parse_IP_packet(rec))
    
    sock_send.close()
    sock_rec.close()


if __name__ == "__main__":
    main("hello")

