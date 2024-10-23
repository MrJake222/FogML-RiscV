#!/usr/bin/env python3

import sys
import time
import struct
import serial

ser = serial.Serial('/dev/ttyACM2', baudrate=1000000)

def prnline(prn=True, end="\n"):
	line = ser.readline().decode("utf-8").strip()
	if prn:
		print(line, end=end)

for i, l in enumerate(sys.stdin):
	for x in l.strip().split():
		x = float(x)
		x = struct.pack("<f", x)
		ser.write(x)
	prnline(prn=False) # storing tick
	
	if (i+1) % 64 == 0:
		prnline() # processing
		prnline() # learning / classifying
		
		start = time.time()
		prnline() # finished / lof score
		end = time.time()
		
		print(f"[P {(i+1)//64:02d}] took: {end - start:.1f} sec")
		print()
