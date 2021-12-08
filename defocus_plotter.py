import os
import sys
import time
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
import statistics
import pickle
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec
import numpy as np
import mrcfile
###set up plot with gridspect to be updated by animate function ###
fig = plt.figure(figsize=(10,10))
spec = gridspec.GridSpec(ncols=4, nrows=14, wspace=2)
###segment the figure in subplots using gridspec specification with numpy slicing###
f1_ax1 = fig.add_subplot(spec[0:-10,:])
f1_ax2 = fig.add_subplot(spec[5:-4,:-2])
###remove ticks from axes###
f1_ax2.set_yticks([])
f1_ax2.set_xticks([])
f1_ax3 = fig.add_subplot(spec[5:-4,2:])
f1_ax3.set_yticks([])
f1_ax3.set_xticks([])
f1_ax4 = fig.add_subplot(spec[10:,:])
###define data to be represented and pass to animation function###
data_x = []
data_y = []
data_x2 = []
data_y2 = []
###master function where data is feed with delay controled by the interval option in the ani object###
def animate(i, data_x, data_y, data_x2, data_y2):
	###capturing data generated by defocus_catcher.py as .pkl files###
	with open('avg_defocus.pkl', 'rb') as f:
		avg_defocus = pickle.load(f)
	with open('PS_ctf_files.pkl', 'rb') as f2:
		list_PS_ctf = pickle.load(f2)	
	with open('resolution_list.pkl', 'rb') as f3:
		resolution_list_local = pickle.load(f3)	
	###open mrc files and transform them to numpy arrays so they can be represented with imgshow later###
	with mrcfile.open(list_PS_ctf[-1]) as emd_1:
		nx, ny, nz = emd_1.header['nx'], emd_1.header['ny'], emd_1.header['nz']
		ctf_np_512_1 = emd_1.data.flatten(order='F').reshape(emd_1.header['nx'], emd_1.header['ny'])
	with mrcfile.open(list_PS_ctf[-2]) as emd_2:
		nx, ny, nz = emd_2.header['nx'], emd_2.header['ny'], emd_2.header['nz']
		ctf_np_512_2 = emd_2.data.flatten(order='F').reshape(emd_2.header['nx'], emd_2.header['ny'])
	###define data to be represented on gridspec pannels###	
	data_x = range(0, len(avg_defocus))
	data_y = avg_defocus
	data_x2 = range(0, len(resolution_list_local))
	data_y2 = resolution_list_local
	
	#Clean defocus plot (on top, ax1) and resolution plot (ax4, bottom)###
	f1_ax1.clear()
	f1_ax4.clear()
	###plot defocus data with horizontal lines for max, min,avg defocus###
	f1_ax1.plot(data_x, data_y, 'ko-')
	f1_ax1.set_ylabel('defocus [um]')
	f1_ax1.tick_params(bottom=False, top=True, labelbottom=False, labeltop=True)
	f1_ax1.yaxis.set_minor_locator(tck.AutoMinorLocator())
	f1_ax1.set_title('image number', y=1.3)
	f1_ax1.hlines(max(data_y), 0, len(data_x), colors='blue', linestyles='dotted', label='max')
	f1_ax1.hlines(min(data_y), 0, len(data_x), colors='red', linestyles='dotted', label='min')
	f1_ax1.hlines(np.mean(data_y), 0, len(data_x), colors='gray', linestyles='dashed', label='avg')
	###numpy array derived from the ctf image displayed with imshow:last image###
	f1_ax2 = fig.add_subplot(spec[5:-4,:-2])
	plt.imshow(ctf_np_512_1, cmap='binary')
	f1_ax2.set_xticks([])
	f1_ax2.set_yticks([])
	f1_ax2.set_title("last image")
	###numpy array derived from the ctf image displayed with imshow:second last image###
	f1_ax3 = fig.add_subplot(spec[5:-4,2:])
	plt.imshow(ctf_np_512_2, cmap='binary')
	f1_ax3.set_xticks([])
	f1_ax3.set_yticks([])
	f1_ax3.set_title("second last image")
	###
	###plot resolution data with horizontal lines for max, min,avg resolution###
	f1_ax4.plot(data_x2, data_y2, 'co-')
	f1_ax4.set_ylabel('resolution [A]')
	f1_ax4.yaxis.set_minor_locator(tck.AutoMinorLocator())
	f1_ax4.set_title('image number', y=-0.5)
	f1_ax4.hlines(max(data_y2), 0, len(data_x2), colors='blue', linestyles='dotted')
	f1_ax4.hlines(min(data_y2), 0, len(data_x2), colors='red', linestyles='dotted')
	f1_ax4.hlines(np.mean(data_y2), 0, len(data_x2), colors='gray', linestyles='dashed')
ani = animation.FuncAnimation(fig, animate, fargs=(data_x, data_y, data_x2, data_y2), interval=500)
plt.show()
