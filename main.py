from ConnectionData import ConnectionData
import create_sockets
import socket
import ip_handler
import random
import httpGet
import threading
import queue
import struct


MAX_SQNC = 4,294,967,295

"""
Evan Hanes
Alan Garcia
19 october 2022
"""
def main(domain: str):
    # set up
    local_ip = create_sockets.getLocalIp()
    domain = "www.david.choffnes.com"
    dest_ip = socket.gethostbyname(domain)
    dest_port = 80
    
    conn = handshake(dest_ip, dest_port, local_ip, domain, "/")

    # algorithm
    data = download(conn)
    #dataString = joinAndWrite(data)
    
    
    
    conn.send_sock.close()
    conn.rec_sock.close()
    
    return data


def getRandomData():
    return random.randbytes(random.randint(1, 100))

def joinAndWrite(downloads:dict) -> str:
    downloads = list(downloads.items())
    downloads.sort(key=lambda i:(i[0], i[1]))
    file = []
    for item in downloads:
        file.append(item.decode())
    return "".join(file)
    
 
"""
This function takes care of the main download part of the code.
It uses a queue and a extra thread to process the data and send ack responses.
"""
def download(conn) -> dict:
    download = [] #sequence Number: RAW DATA
    workList = queue.Queue()
    
    
    # Send GET http request
    packet = httpGet.craftRequest(conn.domain, conn.subdomain)
    packet = ip_handler.make_tcp_header_2( packet , conn.rec_port, conn.dest_port, conn.seq_numb, conn.ack_numb, 10, conn.local_ip, conn.dest_ip, push=True, ack=True)
    packet = ip_handler.make_ip_header(packet, conn.local_ip, conn.dest_ip)
    print(conn.dest_ip, conn.dest_port)
    conn.send_sock.sendto(packet, (conn.dest_ip, conn.dest_port))
    
    
    # create a thread and start
    threading.Thread(target=packetWorkerThread(conn, workList, download)).start()
    
    
    # This is my listener
    while True:
        rec = conn.rec_sock.recv(1500)
        src = rec[12:16]
        thisSourceIP = ip_handler.bytes_to_address(src)
        if thisSourceIP == conn.dest_ip:
            workList.enqueue(rec)
            # check the fin bit is set
            
            if (rec[13] << 7) > 1:
                print("FIN DETECTED, bye byee")
                break
    
    workList.join()
    return download

    

"""
This fucntion process all the incoming packets and resends the ack packets.
It also manages the window size
"""
def packetWorkerThread(conn: ConnectionData, workList: queue, download: list):
    windowSize = 2500
    while True:
        if workList.empty(): 
            continue
        
        packet = workList.dequeue()
        
        # pase the packet
        tcp_packet = ip_handler.parse_IP_packet(packet)
        srcPort, destPort, seqNumber, ackNumber, raw_data, window = ip_handler.parse_TCP_packet(tcp_packet)
        
        # craft the reply
        reply = ip_handler.make_tcp_header_2(b"", conn.rec_port,conn.dest_port, conn.seq_numb, (seqNumber + len(raw_data)) % MAX_SQNC, windowSize, conn.local_ip, conn.dest_ip, ack=True)
        reply = ip_handler.make_ip_header(reply, conn.local_ip,conn.dest_ip)
        
        # send the acknowledgment
        conn.send_sock.sendto(reply, (conn.dest_ip, conn.dest_port))
        
        # append the download
        download.append(raw_data)
        
        # if FINN is detected we say bye
        if (packet[13] << 7) > 1:
                print("Worker Thread, bye byee")
                return download
            
    return download
        
        
            
    
        
"""
TCP handshake
"""
def handshake(dest_ip, dest_port, local_ip, domain, subdomain):
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
    
    

    
    

    
    if not sock_rec or not sock_send:
        raise ValueError("Sockets didn't initialize successfully")
    
    # send the first SYN
    packet = ip_handler.make_tcp_header_2( b'' , rec_port, ext_dest_port, initSqnc, 0, 1, local_ip, dest_ip, syn=True)
    packet = ip_handler.make_ip_header(packet, local_ip, dest_ip)
    sock_send.sendto(packet, (dest_ip, ext_dest_port))
    
    
    # Receive SYN ACK
    while True:
        rec = sock_rec.recv(1500)
        src = rec[12:16]
        thisSourceIP = ip_handler.bytes_to_address(src)
        if thisSourceIP == dest_ip:
            srcPort, destPort, seqNumber, ackNumber, raw_data, window = ip_handler.parse_TCP_packet(ip_handler.parse_IP_packet(rec))
            break
    
    # Send first ACK
    packet = ip_handler.make_tcp_header_2( b"", rec_port, ext_dest_port, ackNumber, seqNumber + 1, 20000, local_ip, dest_ip, ack=True)
    packet = ip_handler.make_ip_header(packet, local_ip, dest_ip)
    sock_send.sendto(packet, (dest_ip, ext_dest_port))
    
    
    
    
    
    
    
    # Create the connection object to send away
    conn = ConnectionData(domain, subdomain, local_ip, dest_ip, ext_dest_port, send_port, rec_port)
    conn.setTCP(ackNumber, seqNumber)
    conn.setBindedSockets(sock_send, sock_rec)
    
    return conn 

    

if __name__ == "__main__":
    main("hello")

