import time
from ConnectionData import ConnectionData
import create_sockets
import socket
import pack_handler
import random
import httpGet
import threading
import queue
import struct


MAX_SQNC = 4294967295

"""
Evan Hanes
Alan Garcia
17 october 2022
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

"""
Randome data creation
"""
def getRandomData():
    return random.randbytes(random.randint(1, 100))

"""
This joins and write the data to a file
"""
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
    packet = pack_handler.make_tcp_header_2( packet , conn.rec_port, conn.dest_port, conn.seq_numb, conn.ack_numb, 10, conn.local_ip, conn.dest_ip, push=True, ack=True)
    packet = pack_handler.make_ip_header(packet, conn.local_ip, conn.dest_ip)
    print(conn.dest_ip, conn.dest_port)
    conn.send_sock.sendto(packet, (conn.dest_ip, conn.dest_port))
    
    
    # create a thread and start
    t2 = threading.Thread(target=packetWorkerThread, args=(conn, workList, download),daemon=False)
    t2.start()

    # This is my listener
    while True:
        rec = conn.rec_sock.recv(1500)
        print("LISTENING FOR INCOMING PACKETS")
        src = rec[12:16]
        thisSourceIP = pack_handler.bytes_to_address(src)
        if thisSourceIP == conn.dest_ip:
            print("FROM SOURCE")
            workList.put(rec)
            # check the fin bit is set
            
            if (len(rec) > 20 and rec[13] << 7) > 1:
                print("FIN DETECTED")
    
    workList.join()
    return download

"""
This fucntion process all the incoming packets and resends the ack packets.
It also manages the window szize
"""
def packetWorkerThread(conn: ConnectionData, workList: queue, download: list):
    print("Worked thread is trying to run")
    windowSize = 2500
    while True:
        if workList.empty(): 
            time.sleep(50)
            print("packetWorkerThread")
            continue
        
        
        packet = workList.get()
        # pase the packet
        tcp_packet = pack_handler.parse_IP_packet(packet)
        srcPort, destPort, seqNumber, ackNumber, raw_data, window = pack_handler.parse_TCP_packet(tcp_packet)
        
        # craft the reply
        newSeqnc = (seqNumber + len(raw_data))
        newSeqnc = newSeqnc % MAX_SQNC
        reply = pack_handler.make_tcp_header_2(b"", conn.rec_port,conn.dest_port, conn.seq_numb, newSeqnc, windowSize, conn.local_ip, conn.dest_ip, ack=True)
        reply = pack_handler.make_ip_header(reply, conn.local_ip,conn.dest_ip)
        
        
        print("Sending Replies!")
        # send the acknowledgment
        conn.send_sock.sendto(reply, (conn.dest_ip, conn.dest_port))
        
        # append the download
        download.append(raw_data)
        
        workList.task_done()
        # if FINN is detected we say bye
        if (packet[13] << 7) > 1:
                print("Worker Thread, FIN Detected")
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
    packet = pack_handler.make_tcp_header_2( b'' , rec_port, ext_dest_port, initSqnc, 0, 1, local_ip, dest_ip, syn=True)
    packet = pack_handler.make_ip_header(packet, local_ip, dest_ip)
    sock_send.sendto(packet, (dest_ip, ext_dest_port))
    
    
    # Receive SYN ACK
    while True:
        rec = sock_rec.recv(1500)
        src = rec[12:16]
        thisSourceIP = pack_handler.bytes_to_address(src)
        if thisSourceIP == dest_ip:
            srcPort, destPort, seqNumber, ackNumber, raw_data, window = pack_handler.parse_TCP_packet(pack_handler.parse_IP_packet(rec))
            break
    
    # Send first ACK
    packet = pack_handler.make_tcp_header_2( b"", rec_port, ext_dest_port, ackNumber, seqNumber + 1, 20000, local_ip, dest_ip, ack=True)
    packet = pack_handler.make_ip_header(packet, local_ip, dest_ip)
    sock_send.sendto(packet, (dest_ip, ext_dest_port))
    
    
    
    
    
    
    
    # Create the connection object to send away
    conn = ConnectionData(domain, subdomain, local_ip, dest_ip, ext_dest_port, send_port, rec_port)
    conn.setTCP(ackNumber, seqNumber)
    conn.setBindedSockets(sock_send, sock_rec)
    
    return conn 

if __name__ == "__main__":
    main("hello")