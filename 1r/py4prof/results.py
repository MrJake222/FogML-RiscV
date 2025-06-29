from data import D, T0, T1, WL

TO_SEC = 1 / 16e6

for Dval, t0, wloop in zip(D, T0, WL):
	dsp = Dval[0][1]
	lof = Dval[0][0]
	summ = dsp + lof
	dist = Dval[1][0]
	ops = Dval[2]
	opsum = sum(Dval[2])
	sqops = Dval[3]
	
	print(t0)
	# print(f"LOF: {lof/1e6:.0f} M")
	# print(f"Dst: {dist/summ*100:.0f}%")
	# print(f"Ops: {opsum/summ*100:.0f}%")
	
	# for op in ops:
		# print(f"& {op/1e6:.1f}")
		# print(f"& {op/wloop:.0f}")
		# print(f"& {op/summ*100:.0f}\\%")
		# print()
		
	for op in sqops:
		print(f"& {op/1e6:.1f}")
		print(f"& {op/wloop:.0f}")
		print(f"& {op/summ*100:.0f}\\%")
		print()
	
	dsp *= TO_SEC
	lof *= TO_SEC
	summ *= TO_SEC
	dsp_share = dsp / summ
	# print(f"& {dsp:.2f}")
	# print(f"& {lof:.2f}")
	# print(f"& {summ:.2f}")
	# print(f"& {dsp_share*100:.0f}\\%")

	print()
	# break
