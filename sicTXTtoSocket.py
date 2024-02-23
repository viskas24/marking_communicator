import csv
import re
import argparse
import os.path
import socket


parser = argparse.ArgumentParser()
parser.add_argument('taskpath')
parser.add_argument('socketip')

print(parser.parse_args())
argv = parser.parse_args()

#read sic charmam
charmapfile = open(os.path.join(os.path.dirname(__file__),'charmap.csv'), encoding="UTF-8")
charmapreader = csv.reader(charmapfile, delimiter=';')

charmap = {}

for byte, *symbols in charmapreader:
    for symbol in symbols:
        if symbol:
            charmap[symbol] = int(byte)


#open task text
f = open(argv.taskpath, 'r', errors='replace', encoding="UTF-8")


# configure connections (the parameters differs on the device you are connecting to)
HOST = argv.socketip  # The remote host
PORT = 8899
print(argv.socketip)         # check which port was really used


#check version then send line by line from txt file
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    s.sendall(b'GETVERSION\r\n')  # load file to e10
    getversionanswer = s.recv(1024)
    print(getversionanswer)
    version = tuple(
        int(x) for x in re.match(b'GETVERSION e(\d+)v(\d+)-(\d+)-(\d+)', getversionanswer).group(1, 2, 3, 4))
    print(version)

    for line in f.readlines():
        line = line.rstrip()

        command = line.split(' ',1)[0]
        if command=='SETVAR' and version >= (10, 0):
            #line.split(' ',2)[2].replace(' ','№')
            args = line.split(' ',2)
            args[2] = args[2].replace(' ','№')
            line = ' '.join(args)
        else:
            pass #e8 version
        print(line)

        translated = bytearray()

        #change char by sic charmap
        for symbol in line.rstrip():
            translated.append(charmap[symbol])

        translated+=b'\r\n'
        s.sendall(translated)  # load line to e10
        print(translated)
        data = s.recv(1024)
        print(data)
    s.close()

