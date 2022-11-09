import ip_handler
from main import ConnectionData

def tcpACK(conn: ConnectionData):
    packet = ip_handler.make_tcp_header_2( b"", conn.rec_port, conn.dest_port, (conn.seq_numb + 1) % 0xFFFFFFFF, conn.ack_numb, 10, False, True, False, conn.local_ip, conn.dest_ip)
    packet = ip_handler.make_ip_header(packet, conn.local_ip, conn.dest_ip)
    return packet
    
def tcpSYN(conn: ConnectionData, data):
    packet = ip_handler.make_tcp_header_2( data, conn.rec_port, conn.dest_port, (conn.seq_numb + len(data)) % 0xFFFFFFFF, conn.ack_numb, 10, True, False, False, conn.local_ip, conn.dest_ip)
    packet = ip_handler.make_ip_header(packet, conn.local_ip, conn.dest_ip)
    return packet