import socket
import sys


def client(msg, log_buffer=sys.stderr):
    """client opens a socket, sends the input msg and receives the same message back 16 bytes at a chunk"""

    server_address = ('localhost', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)
    print('connecting to {0} port {1}'.format(*server_address), file=log_buffer)
    sock.connect(server_address)
    received_message = ''
    try:
        print('sending "{0}"'.format(msg), file=log_buffer)
        sock.sendall(msg.encode('utf-8'))
        while True:
            chunk = sock.recv(16)
            print('received "{0}"'.format(chunk.decode('utf8')), file=log_buffer)
            received_message = received_message + chunk.decode('utf8')
            if len(chunk) < 16:
                break
            # for breaking the loop if the byte count is exactly 16.  Probably a better way...
            if msg == received_message:
                break
    finally:
        print('closing socket', file=log_buffer)
        sock.close()
    return received_message


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage = '\nusage: python echo_client.py "this is my message"\n'
        print(usage, file=sys.stderr)
        sys.exit(1)

    msg = sys.argv[1]
    client(msg)
