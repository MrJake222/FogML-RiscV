#!/usr/bin/env python3

import sys
import time
import struct
import serial

ser = serial.Serial('/dev/ttyACM2', baudrate=1000000)

def getline(prn=True, end="\n"):
	line = ser.readline().decode("utf-8").strip()
	if prn:
		print(line, end=end)
	return line

for i, l in enumerate(sys.stdin):
	for x in l.strip().split():
		x = float(x)
		x = struct.pack("<f", x)
		ser.write(x)
	getline(prn=False) # storing tick
	
	if (i+1) % 64 == 0:
		getline() # processing
		lc = getline() # learning / classifying
		
		start = time.time()
		if lc.startswith("learning"):
			getline() # DSP time
			getline() # RES time
			getline() # LOF time
		getline() # finished / lof score
		end = time.time()
		print(f"[P {(i+1)//64:02d}] lof took: {end - start:.1f} sec")

		start = time.time()
		getline() # RF DSP
		getline() # RF cls
		getline() # RF result
		end = time.time()
		print(f"[P {(i+1)//64:02d}] rf took: {end - start:.1f} sec")
		print()
