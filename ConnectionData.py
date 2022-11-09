"""
    This class holds the properties of a connection. 
"""
class ConnectionData:
    def __init__(self, domain, subdomain, local_ip, dest_ip, dest_port, send_port, rec_port):
        self.domain = domain
        self.subdomain = subdomain
        self.local_ip = local_ip
        self.dest_ip = dest_ip
        self.dest_port = dest_port
        self.send_port = send_port
        self.rec_port = rec_port
        self.seq_numb = None
        self.ack_numb = None
        self.send_sock = None
        self.rec_sock = None
        return

    def setTCP(self, seq_numb, ack_numb):
        self.seq_numb = seq_numb
        self.ack_numb = ack_numb
        return
    
    def setBindedSockets(self, send_sock, rec_sock):
        self.send_sock = send_sock
        self.rec_sock = rec_sock
        return
