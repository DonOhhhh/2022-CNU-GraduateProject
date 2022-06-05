import socket, json

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('localhost', 5001))
print(f'Listening on {sock}')
start = 0
end = 0
while True:
    try:
        if start and end:
            print('Recorded Zygote init time!')
            with open('result.txt','a') as f:
                f.write(f'ZygoteInit exec time : {end - start}ms')
            start = 0
            end = 0

        data, client = sock.recvfrom(1500)
        flag, time = data.decode('utf-8').split(' ')
        if flag == 'start':
            start = int(time)
            print(f'Zygote started time : {start}')
        elif flag == 'end':
            end = int(time)
            print(f'Zygote ended time : {end}')
    except KeyboardInterrupt:
        print(f'Shutting down... {sock}')
        break
