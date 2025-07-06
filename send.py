#!/usr/bin/env python3

import sys
import time
import struct
import serial

if len(sys.argv) == 3:
	PORT = sys.argv[2]
elif len(sys.argv) == 2:
	PORT = "/dev/ttyACM2"
else:
	print(f"usage: {sys.argv[0]} [reservoir fill level]")
	exit(1)

ser = serial.Serial(PORT, baudrate=1000000)
FILL_SAMPLES = int(sys.argv[1])
EOT = 0x04

print(f"Opening port {PORT} and sending {FILL_SAMPLES} samples")

req = bytes()
for i, l in enumerate(sys.stdin, start=1):
	for x in l.strip().split():
		req += struct.pack("<f", float(x))
	
	if i % 64 == 0:
		samples = i//64
		if samples < FILL_SAMPLES:
			action = 'R'
		elif samples == FILL_SAMPLES:
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
		
		# print()
