import create_sockets as my_socks
import socket
import ip_handler
import random
import httpGet
import threading
import queue

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
    sendSoc, recSoc = handshake(dest_ip, dest_port, local_ip, domain, "/")
    
    
    sendSoc.close()
    recSoc.close()
    
    
def download(conn: Connection):
    conn = Connection()
    download = {} #sequence Number: RAW DATA
    workList = queue.Queue()
    
    # Send GET http request
    packet = httpGet.craftRequest(conn.domain, conn.subdomain)
    packet = ip_handler.make_tcp_header_2(packet , conn.rec_port, conn.dest_port, conn.seq_numb + 1, conn.ack_numb + 1, 1, True, False, False, conn.local_ip, conn.dest_ip)
    packet = ip_handler.make_ip_header(packet, conn.local_ip, conn.dest_ip)
    conn.send_sock.sendto(packet, (conn.dest_ip, conn.dest_port))
    
    
    window = 1
    # create a thread that listens to all
    while len(workList > 0):
        pass
    
    
    # wait until both processes are done
    workList.join()
    
    
    return download
    
    
    


def packetReciever(sock: socket, workList: queue):
    
    fin = False;
    while not fin:
        packet = sock.recv(1500)
        workList.enqueue
    pass
    
    
        
    
def handshake(dest_ip, dest_port, local_ip, domain, subdomain):
    # HANDSHAKE
    
    ext_dest_port = dest_port
    
    
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
    
    
    # Send the Ack
    packet = ip_handler.make_tcp_header_2( b"", rec_port, ext_dest_port, ackNumber + 1, seqNumber + 1, 1, False, True, False, local_ip, dest_ip)
    packet = ip_handler.make_ip_header(packet, local_ip, dest_ip)
    sock_send.sendto(packet, (dest_ip, ext_dest_port))
    
    """
    rec = sock_rec.recv(1500)
    srcPort, destPort, seqNumber, ackNumber, raw_data, window = ip_handler.parse_TCP_packet(ip_handler.parse_IP_packet(rec))
    """
    con = Connection(domain, subdomain, local_ip, dest_ip, ext_dest_port, send_port, rec_port)
    con.setTCP(initSqnc + 1, seqNumber + 1)
    con.setBindedSockets(sock_send, sock_rec)
    return con
    
    
    

"""
    This class holds the properties  of a connection. 
"""
class Connection():
  def __init__(self, domain, subdomain, local_ip, dest_ip, dest_port, send_port, rec_port):
    self.domain = domain
    self.subdomain = subdomain
    self.local_ip = local_ip
    self.dest_ip = dest_ip
    self.dest_port = dest_port
    self.send_port = send_port
    self.rec_port = rec_port
    return

def setTCP(self, seq_numb, ack_numb):
    self.seq_numb = seq_numb
    self.ack_numb = ack_numb
    return
    
def setBindedSockets(self, send_sock, rec_sock):
    self.send_sock = send_sock
    self.rec_sock = rec_sock
    return

    

if __name__ == "__main__":
    main("hello")

