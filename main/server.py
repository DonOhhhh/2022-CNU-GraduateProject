import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('localhost', 5001))
print(f'Listening on {sock}')
start = 0
end = 0
while True:
    try:
        data, client = sock.recvfrom(1500)
        if start == 0:
            start = data.decode('utf-8')
        elif end == 0:
            end == data.decode('utf-8')
        if start != 0 and end != 0:
            with open('result.txt','a') as f:
                f.write(f'ZygoteInit 실행시간 : {end - start}ms')
            start = 0
            end = 0
    except KeyboardInterrupt:
        print(f'Shutting down... {sock}')
        break
