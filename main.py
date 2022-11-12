#!/usr/bin/env python3
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
    data = download_S(conn)
    
    #dataString = joinAndWrite(data)
    if len(data) > 0:
        joinAndWrite(data)
    
    return data

"""
Randome data creation
"""
def getRandomData():
    return random.randbytes(random.randint(1, 100))

"""
This joins and write the data to a file
"""
def joinAndWrite(data:bytes) -> str:

    f = open("index.html", "xb")
    for char in data:
        f.write(char)
    f.close()

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
        print("LISTENING FOR INCOMING PACKETS" + str(workList.qsize()))
        src = rec[12:16]
        thisSourceIP = pack_handler.bytes_to_address(src)
        #TODO check the port also
        if thisSourceIP == conn.dest_ip:
            workList.put(rec)
            # check the fin bit is set
            
            #0000 0001 << 7 = 1000 0000 if that is > 0
            if len(rec) > 20 and ((packet[20+13] << 7) > 1):
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
        if len(packet) > 20 and ((packet[13] << 7) > 1):
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

"""
Close tcp connections
"""
def closeTCP(conn: ConnectionData):
    reply = pack_handler.make_tcp_header_2(b"", conn.rec_port,conn.dest_port, conn.seq_numb, conn.ack_numb, 1, conn.local_ip, conn.dest_ip, fin=True, ack=True)
    reply = pack_handler.make_ip_header(reply, conn.local_ip,conn.dest_ip)
    conn.send_sock.sendto(reply, (conn.dest_ip, conn.dest_port))
    conn.rec_sock.close()
    conn.send_sock.close()
    
    
"""
This function takes care of the main download part of the code.
It uses a single thread
"""
def download_S(conn: ConnectionData) -> dict:
    download = [] #sequence Number: RAW DATA
    
    
    # Send GET http request
    packet = httpGet.craftRequest(conn.domain, conn.subdomain)
    packet = pack_handler.make_tcp_header_2( packet , conn.rec_port, conn.dest_port, conn.seq_numb, conn.ack_numb, 10, conn.local_ip, conn.dest_ip, push=True, ack=True)
    packet = pack_handler.make_ip_header(packet, conn.local_ip, conn.dest_ip)
    print(conn.dest_ip, conn.dest_port)
    conn.send_sock.sendto(packet, (conn.dest_ip, conn.dest_port))
    
    # This is my listener
    while True:
        rec = conn.rec_sock.recv(1500)
        src = rec[12:16]
        thisSourceIP = pack_handler.bytes_to_address(src)
        incomingPort = int(struct.unpack('>H', rec[20+2:20+4])[0])
        
        if thisSourceIP == conn.dest_ip and conn.rec_port == incomingPort:
            respondPacket(conn, rec, download)
            # check the fin bit is set
            
            #0000 0001 << 7 = 1000 0000 if that is > 0
            if checkFinBit(rec[33]):
                closeTCP(conn)
                return download
    
    
    return download

"""
This fucntion process all the incoming packets and resends the ack packets.
It also manages the window szize
"""
def respondPacket(conn: ConnectionData, packet: bytes, download: list):
    
    windowSize = 5832
        # pase the packet
    tcp_packet = pack_handler.parse_IP_packet(packet)
    srcPort, destPort, seqNumber, ackNumber, raw_data, window = pack_handler.parse_TCP_packet(tcp_packet)
    
    # craft the reply
    newSeqnc = (seqNumber + len(raw_data))
    newSeqnc = newSeqnc % MAX_SQNC
    conn.seq_numb += 1
    reply = pack_handler.make_tcp_header_2(b"", conn.rec_port,conn.dest_port, conn.seq_numb, newSeqnc, windowSize, conn.local_ip, conn.dest_ip, ack=True)
    reply = pack_handler.make_ip_header(reply, conn.local_ip,conn.dest_ip)
    
    
    
    # send the acknowledgment
    conn.send_sock.sendto(reply, (conn.dest_ip, conn.dest_port))
    print("Reply Sent")
    # append the download
    download.append(raw_data)
    
    
            
    return download

def checkFinBit(currByte: bytes):
    #int.from_bytes(currByte, "big")
    res = True if ( currByte & 0b0001) > 0 else False
    print(currByte, res)
    return res


if __name__ == "__main__":
    main("hello")
    
    
    
    