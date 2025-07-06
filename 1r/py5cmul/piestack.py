import matplotlib.pyplot as plt
import numpy as np
from math import pi

from data import D, T0, T1, sumL0

figsize = 10
fontsize = 9
fontsize2 = 16
size = 0.2
Radius = 0.9

fig, ax = plt.subplots(2, 2, figsize=(figsize, figsize), tight_layout=True)

for axi, (ax, L, t0) in enumerate(zip(ax.flat, D, T0)):
	norm0 = sumL0 / (2*pi)

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

	for i, (l, T1val) in enumerate(zip(L, T1)):
		if i == 0:
			color1_inside, color1_frame = colors_drawio[color_index]
			color2_inside, color2_frame = colors_drawio[color_index+1]
			colors = [color1_inside, color2_inside, color_inactive]
			color_index += 2
			color_frame = color1_frame
		elif i == 3 and axi > 0:
			continue
		else:
			color_inside, color_frame = colors_drawio[color_index]
			colors = [color_inside]*(len(l) - 1) + [color_inactive]
			color_index += 1
		
		radius = Radius - size*i
		wedges, txts, pcts = ax.pie(l, radius=radius, wedgeprops=dict(width=size, edgecolor=color_frame), colors=colors, autopct='%1.0f%%')
		
		if i == 0:
			wedges[1].set_edgecolor(color2_frame)
				
		pctdist = radius - size/2
		for j, (txt, pct, t1) in enumerate(zip(txts, pcts, T1val)):
			xi, yi = pct.get_position()
			phi = np.arctan2(yi, xi)
			d = pctdist
			if (i == 2 and j == 0) or i == 3:
				d -= 0.015
			x = d * np.cos(phi)
			y = d * np.sin(phi)
			
			txt.set_text(t1)
			
			txt.set_position((x, y+0.06/2))
			pct.set_position((x, y-0.06/2))
			
			txt.set(ha='center', va='center')
			pct.set(ha='center', va='center')
			
			txt.set_fontsize(fontsize)
			pct.set_fontsize(fontsize)
			
		txts[-1].set_text("")
		pcts[-1].set_text("")
		
		if i == 2:
			# last ring: square/accum/etc.
			for j in range(axi):
				txts[j].set_text("")
				pcts[j].set_text("")
	
	ax.set_title(t0)
	ax.title.set_fontsize(fontsize2)
	ax.set_ylim(-1,1)
	ax.set_xlim(-1,1)
	
	ax.set(aspect="equal")
	ax.set_axis_off()

plt.savefig("prof5.pdf", bbox_inches='tight', pad_inches=0)
