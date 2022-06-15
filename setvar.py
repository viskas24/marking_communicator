import time
import serial
import argparse
import os.path

parser = argparse.ArgumentParser()
parser.add_argument('filename')
parser.add_argument('varname')
parser.add_argument('vardata')
parser.add_argument('comport')

print(parser.parse_args())
argv = parser.parse_args()

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(argv.comport)  # open serial port
print(ser.name)                    # check which port was really used

print ('GETVERSION')
ser.write(b'GETVERSION\r\n')
time.sleep(0.5)

getversionanswer = ser.read_all()
print(getversionanswer)
time.sleep(0.5)

filename = argv.filename.encode('utf-8')
setvar = argv.varname.encode('utf-8') + b' ' + argv.vardata.encode('utf-8')

ser.write(b'LOADFILE '+ filename + b'\r\n')
ser.write(b'SETVAR '+ setvar + b'\r\n')
time.sleep(0.5)

ser.close()             # close port
