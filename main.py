import create_sockets as my_socks
import socket
import ip_handler
import random
import httpGet

"""
Evan Hanes
Alan Garcia
19 october 2022
"""

def getRandomData():
    return random.randbytes(random.randint(1, 100))


def main(domain: str):
    # set up
    local_ip = my_socks.getLocalIp();
    domain = "www.david.choffnes.com"
    dest_ip = socket.gethostbyname(domain)
    dest_port = 80
    sendS, recS,  handshake(dest_ip, dest_port, local_ip, domain)
    
    
    sock_send.close()
    sock_rec.close()
    
    
    
    
    
    
        
    
def handshake(dest_ip, dest_port, local_ip, domain):
    # HANDSHAKE
    
    ext_dest_port = dest_port;
    
    
    rec_port = random.randint(10000, 65000)
    send_port = random.randint(10000, 65000)
    
    
    while rec_port == send_port:
        rec_port = random.randint(10000, 65000)
        send_port = random.randint(10000, 65000)
    
    
    
    
    initSqnc = random.randint(10000, 65000)
    print(f'Local ip {local_ip}:{send_port}, destination ip {dest_ip }:{ext_dest_port}, rec port: {rec_port}')
    sock_send = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    sock_rec = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    
    packet = ip_handler.make_tcp_header_2( b'' , rec_port, ext_dest_port, initSqnc, 0, 1, True, False, False, local_ip, dest_ip)
    packet = ip_handler.make_ip_header(packet, local_ip, dest_ip)

    
    # Set socket options and bind them to their respective ports
    sock_send.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    sock_send.bind((local_ip, send_port))
    sock_rec.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    sock_rec.bind((local_ip, rec_port))

    
    if not sock_rec or not sock_send:
        raise ValueError("Sockets didn't initialize successfully")
    
    
    
    sock_send.sendto(packet, (dest_ip, ext_dest_port))
    
    
    rec = sock_rec.recv(1500)
    srcPort, destPort, seqNumber, ackNumber, raw_data, window = ip_handler.parse_TCP_packet(ip_handler.parse_IP_packet(rec))
    
    getPacket = httpGet.craftRequest(domain, "/")
    # Send the Ack
    packet = ip_handler.make_tcp_header_2( b"", rec_port, ext_dest_port, initSqnc + 1, seqNumber + 1, 1, False, True, False, local_ip, dest_ip)
    packet = ip_handler.make_ip_header(packet, local_ip, dest_ip)
    sock_send.sendto(packet, (dest_ip, ext_dest_port))
    
    rec = sock_rec.recv(1500)
    srcPort, destPort, seqNumber, ackNumber, raw_data, window = ip_handler.parse_TCP_packet(ip_handler.parse_IP_packet(rec))
    return sock_send, sock_rec
    
    
    

if __name__ == "__main__":
    main("hello")

