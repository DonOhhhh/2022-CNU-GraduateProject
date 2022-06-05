import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('localhost', 5001))
print(f'Listening on {sock}')
while True:
    try:
        data, client = sock.recvfrom(1500)
        print(data.decode('utf-8'))
    except KeyboardInterrupt:
        print(f'Shutting down... {sock}')
        break