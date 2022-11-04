import socket
import socket_metadata as sm


def main():

    # Get the destination IP address
    dest_ip = socket.gethostbyname("david.choffnes.com")
    
    # Create send and receive raw sockets and bind them to 
    # the ephemeral ports.
    metadata = sm.get_metadata()
    local_ip = metadata[0]
    send_port = metadata[1]
    rec_port = metadata[2]

    send_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    send_sock.bind((local_ip, send_port))

    rec_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    rec_sock.bind((local_ip, rec_port))


if __name__ == "__main__":
    main()