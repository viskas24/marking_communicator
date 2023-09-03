#I'm sorry for bad code


import socket

file = open ('TEST.sicmf', 'rb') # File you need to copy to SIC controller

line=file.readline()


HOST = '192.168.1.79'    # The remote host
PORT = 8899              # The same port as used by the server

print(line)
l=len(line)
print(l)                # length for sicmf file

l=l+13
h=hex(l)
print(h)                # length + 13 (filename) in hex 

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'\x02\x00\x35\x47\x00\x5c' + b'SAMPLE' + b'\x00\x00\x00\x00\x00\x00\x02'+ line + b'\x03') # load file to e10

#   '\x02\x00\x35\x47' - fixed command
#   '\x00\x5c' - change to your 'h'
#    length for filename =11. unused letter = \x00
#    SAMPLE = 6 letter + 5'\x00' + fixed '\x00\x02'

    data = s.recv(1024)
    print('Received', repr(data))      # test message from e10
