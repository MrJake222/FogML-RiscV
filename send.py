#!/usr/bin/env python3

import sys
import time
import struct
import serial

ser = serial.Serial('/dev/ttyACM3', baudrate=1000000)

EOT = 0x04

req = bytes()
for i, l in enumerate(sys.stdin, start=1):
	for x in l.strip().split():
		req += struct.pack("<f", float(x))
	
	if i % 64 == 0:
		if i//64 < 16:
			action = 'L'
		else:
			action = 'C'

		req += action.encode("utf-8")
		ser.write(req)
		req = bytes()
		
		while True:
			line = ser.readline()
			if line[0] == EOT:
				break
			print(line.decode("utf-8").strip())
		
		print()
