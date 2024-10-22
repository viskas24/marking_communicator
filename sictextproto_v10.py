import time
import serial
import csv
import re
import argparse
import os.path

parser = argparse.ArgumentParser()
parser.add_argument('taskpath')
parser.add_argument('comport')

print(parser.parse_args())
argv = parser.parse_args()

charmapfile = open(os.path.join(os.path.dirname(__file__),'charmap.csv'), encoding="UTF-8")
charmapreader = csv.reader(charmapfile, delimiter=';')

charmap = {}

for byte, *symbols in charmapreader:
    for symbol in symbols:
        if symbol:
            charmap[symbol] = int(byte)


#timeout = 1000

#f = open(argv.taskpath, 'r', errors='replace', encoding="UTF-8")
f = open(argv.taskpath, 'r', errors='replace', encoding="ANSI")


# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(argv.comport)  # open serial port
print(ser.name)         # check which port was really used

inputt=1
answer =b''

print ('GETVERSION')
ser.write(b'GETVERSION\r\n')
time.sleep(0.3)
getversionanswer = ser.read_all()
#getversionanswer = (b'GETVERSION e10v1-2-3\r')


print(getversionanswer)
version = tuple(int(x) for x in re.match(b'GETVERSION e(\d+)v(\d+)-(\d+)-(\d+)', getversionanswer).group(1,2,3,4))
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
        pass #версия для e8
    print(line)

    translated = bytearray()

    for symbol in line.rstrip():
        translated.append(charmap[symbol])

    translated+=b'\r\n'
    ser.write(translated)


    time.sleep(0.3)
    answer = ser.read_all()
    print(answer)

ser.close()             # close port


