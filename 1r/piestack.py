import matplotlib.pyplot as plt
import numpy as np
from math import pi

D = [[None]*4 for _ in range(4)]

# no fft, learn
D[0][0] = [285662099, 286200*100]
D[0][1] = [279132313]
D[0][2] = [173431310, 42300247, 29961318, 21966438]
D[0][3] = [102770164, 49969747]

# no fft, infer
D[1][0] = [3171216, 286200]
D[1][1] = [3120137]
D[1][2] = [2013586, 457020, 312691, 221340]
D[1][3] = [1197050, 582536]

# with fft, learn
D[2][0] = [374255132, 1350987*100]
D[2][1] = [367720912]
D[2][2] = [225240588, 60844765, 43191585, 21964574]
D[2][3] = [132949538, 64537051]

# with fft, infer
D[3][0] = [4632413, 1350987]
D[3][1] = [4581680]
D[3][2] = [3029272, 693210, 472218, 221080]
D[3][3] = [1798288, 879984]

T = [None]*4
T[0] = ["Learn", "DSP"]
T[1] = ["Dist"]
T[2] = ["Square", "Diff", "Accum", "Sqrt"]
T[3] = ["Mul64", "Norm"]

T2 = [None]*4
T2[0] = "Learn (no FFT)"
T2[1] = "Infer (no FFT)"
T2[2] = "Learn (FFT)"
T2[3] = "Infer (FFT)"

figsize = 10
fontsize = 9
fontsize2 = 16
size = 0.2
Radius = 0.9

fig, ax = plt.subplots(2, 2, figsize=(figsize, figsize), tight_layout=True)

for ax, L, t2 in zip(ax.flat, D, T2):
	norm0 = sum(L[0]) / (2*pi)

	for l in L:
		for i in range(len(l)):
			l[i] /= norm0
		left = 2*pi - sum(l)
		l.append(abs(left))

	# print(*L, sep="\n")
	
	colors_drawio = [
		#  inside,    frame
		["#dae8fc", "#6c8ebf"],
		["#d5e8d4", "#82b366"],
		["#ffe6cc", "#d79b00"],
		["#fff2cc", "#d6b656"],
		["#f8cecc", "#b85450"],
		["#e1d5e7", "#9673a6"],
	]
	color_index = 0
	color_inactive = "#FFFFFF"

	for i, (l, t) in enumerate(zip(L, T)):
		if i == 0:
			color1_inside, color1_frame = colors_drawio[color_index]
			color2_inside, color2_frame = colors_drawio[color_index+1]
			colors = [color1_inside, color2_inside]
			color_index += 2
			color_frame = color1_frame
		else:
			color_inside, color_frame = colors_drawio[color_index]
			colors = [color_inside]*(len(l) - 1) + [color_inactive]
			color_index += 1
		
		radius = Radius - size*i
		wedges, txts, pcts = ax.pie(l, radius=radius, wedgeprops=dict(width=size, edgecolor=color_frame), colors=colors, autopct='%1.0f%%')
		
		if i == 0:
			wedges[1].set_edgecolor(color2_frame)
				
		pctdist = radius - size/2
		for j, (txt, pct, txt_val) in enumerate(zip(txts, pcts, t)):
			xi, yi = pct.get_position()
			phi = np.arctan2(yi, xi)
			d = pctdist
			if (i == 2 and j == 0) or i == 3:
				d -= 0.015
			x = d * np.cos(phi)
			y = d * np.sin(phi)
			
			txt.set_text(txt_val)
			
			txt.set_position((x, y+0.06/2))
			pct.set_position((x, y-0.06/2))
			
			txt.set(ha='center', va='center')
			pct.set(ha='center', va='center')
			
			txt.set_fontsize(fontsize)
			pct.set_fontsize(fontsize)
			
		txts[-1].set_text("")
		pcts[-1].set_text("")
	
	ax.set_title(t2)
	ax.title.set_fontsize(fontsize2)
	ax.set_ylim(-1,1)
	ax.set_xlim(-1,1)
	
	ax.set(aspect="equal")
	ax.set_axis_off()

plt.savefig("prof.pdf", bbox_inches='tight', pad_inches=0)
