import socket

def get_metadata():
    """
    Gets the local IP address and two free ports to be assigned 
    to the raw sockets. Returns a tuple in the form 
    (local_IP, send_port, rec_port).
    """

    # Create ephemeral port to get send raw socket port and 
    #local IP address.
    eph_sock_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    eph_sock_1.connect(("david.choffnes.com", 80))
    eph_sock_1.sendall(b"HI")
    local_IP = eph_sock_1.getsockname()[0]
    send_port = eph_sock_1.getsockname()[1]
    eph_sock_1.close()

    # Create ephemeral socket to find port for receive socket.
    eph_sock_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    eph_sock_2.connect(("david.choffnes.com", 80))
    eph_sock_2.sendall(b"HI")
    rec_port = eph_sock_2.getsockname()[1]
    eph_sock_2.close()

    return (local_IP, send_port, rec_port)

if __name__ == "__main__":
    get_metadata()