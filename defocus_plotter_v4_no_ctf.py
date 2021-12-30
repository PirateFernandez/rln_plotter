
import os
import sys
import time
import matplotlib.pyplot as plt
import statistics
import pickle
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec
import numpy as np
#import mrcfile
###set up the plot with gridspect that is going to updated###
fig = plt.figure(figsize=(15,15))
spec = gridspec.GridSpec(ncols=8, nrows=16, wspace=2)
###segment the figure in subplots using gridspec specification with numpy slicing###
### ax1 -> top left plot all defocus/img-number ###
f1_ax1 = fig.add_subplot(spec[0:-13,:-4])
### ax2 -> left plot last 48 defocus/img-number ###
f1_ax2 = fig.add_subplot(spec[4:-9,:-6])
### ax3 -> left plot last 32 defocus/img-number ###
f1_ax3 = fig.add_subplot(spec[4:-9,2:-4])
### ax4 -> top left plot all resolution/img-number ###
f1_ax4 = fig.add_subplot(spec[8:-5,:-4])
### ax5 -> top right hist all defocus###
f1_ax5 = fig.add_subplot(spec[0:-13,4:-2])
### ax6 -> left plot last 48 resolution/img-number ###
f1_ax6 = fig.add_subplot(spec[8:-5,4:-2])
f1_ax7 = fig.add_subplot(spec[4:-9,4:-2])
f1_ax8 = fig.add_subplot(spec[12:-1,:-6])
f1_ax9 = fig.add_subplot(spec[12:-1,2:-4])
f1_ax10 = fig.add_subplot(spec[12:-1,4:-2])
#polar
f1_ax11 = fig.add_subplot(spec[0:-13,6:], projection='polar')
f1_ax11.set_xticklabels([])
#f1_ax11.set_yticklabels([])
f1_ax12 = fig.add_subplot(spec[4:-9,6:], projection='polar')
f1_ax12.set_xticklabels([])
#f1_ax12.set_yticklabels([])
f1_ax13 = fig.add_subplot(spec[8:-5,6:], projection='polar')
f1_ax13.set_xticklabels([])
#f1_ax13.set_yticklabels([])
f1_ax14 = fig.add_subplot(spec[12:-1,6:], projection='polar')
f1_ax14.set_xticklabels([])
#f1_ax14.set_yticklabels([])
###define data to be represented and pass to animation function###
data_x = []
data_y = []
data_x2 = []
data_y2 = []
###master function where data is feed with delay controled by the interval option in the animation object.###
def animate(i, data_x, data_y, data_x2, data_y2):
	###capturing data generated by defocus_catcher.py as .pkl files###
	with open('avg_defocus.pkl', 'rb') as f:
		avg_defocus = pickle.load(f)
	#with open('PS_ctf_files.pkl', 'rb') as f2:
	#	list_PS_ctf = pickle.load(f2)	
	with open('resolution_list.pkl', 'rb') as f3:
		resolution_list_local = pickle.load(f3)	
	with open('azymuth.pkl', 'rb') as f4:
		azymuth_list = pickle.load(f4)
	with open('defocus_dif.pkl', 'rb') as f5:
		defocus_dif_list = pickle.load(f5)
	###open mrc files and transform them to numpy arrays so they can be represented with imgshow later###
	#with mrcfile.open(list_PS_ctf[-2]) as emd_1:
	#	nx, ny, nz = emd_1.header['nx'], emd_1.header['ny'], emd_1.header['nz']
	#	ctf_np_512_1 = emd_1.data.flatten(order='F').reshape(emd_1.header['nx'], emd_1.header['ny'])
	#with mrcfile.open(list_PS_ctf[-3]) as emd_2:
	#	nx, ny, nz = emd_2.header['nx'], emd_2.header['ny'], emd_2.header['nz']
	#	ctf_np_512_2 = emd_2.data.flatten(order='F').reshape(emd_2.header['nx'], emd_2.header['ny'])
	#with mrcfile.open(list_PS_ctf[-4]) as emd_3:
	#	nx, ny, nz = emd_3.header['nx'], emd_3.header['ny'], emd_3.header['nz']
	#	ctf_np_512_3 = emd_3.data.flatten(order='F').reshape(emd_3.header['nx'], emd_3.header['ny'])
	###define data to be represented on gridspec pannels###	
	data_x = range(0, len(avg_defocus))
	data_y = avg_defocus
	pc10_data_y = round((-(len(data_y)*10)/100))
	pc20_data_y = round((-(len(data_y)*20)/100))
	pc30_data_y = round((-(len(data_y)*30)/100))
	data_x2 = range(0, len(resolution_list_local))
	data_y2 = resolution_list_local
	pc10_data_y2 = round((-(len(data_y2)*10)/100))
	pc20_data_y2 = round((-(len(data_y2)*20)/100))
	pc30_data_y2 = round((-(len(data_y2)*30)/100))
	data_x3 = defocus_dif_list
	pc10_data_x3 = round((-(len(data_x3)*10)/100))
	pc20_data_x3 = round((-(len(data_x3)*20)/100))
	pc30_data_x3 = round((-(len(data_x3)*30)/100))
	data_y3 = azymuth_list
	pc10_data_y3 = round((-(len(data_y3)*10)/100))
	pc20_data_y3 = round((-(len(data_y3)*20)/100))
	pc30_data_y3 = round((-(len(data_y3)*30)/100))
	
	#Clean defocus plot (on top, ax1) and resolution plot (ax4, bottom)###
	f1_ax1.clear()
	f1_ax2.clear()
	f1_ax3.clear()
	f1_ax4.clear()
	f1_ax5.clear()
	f1_ax6.clear()
	f1_ax7.clear()	
	f1_ax8.clear()
	f1_ax9.clear()	
	f1_ax10.clear()
	###plot defocus data with horizontal lines for max, min,avg defocus###
	f1_ax1.plot(data_x, data_y, 'o-', color='slateblue', lw=0.2, ms=2)
	f1_ax1.set_ylabel('defocus [um]')
	f1_ax1.set_ylim([0,3])
	f1_ax1.tick_params(bottom=True, top=False, labelbottom=True, labeltop=False)
	f1_ax1.set_title('image number all', y=1)
	f1_ax1.hlines(max(data_y), 0, len(data_x), colors='blue', linestyles='dotted', label='max')
	f1_ax1.hlines(min(data_y), 0, len(data_x), colors='red', linestyles='dotted', label='min')
	f1_ax1.hlines(np.mean(data_y), 0, len(data_x), colors='dimgray', linestyles='dashed', label='avg')
	###numpy array derived from the ctf image displayed with imshow:last image###
	#if len(avg_defocus) > 300 :	
	#f1_ax2 = fig.add_subplot(spec[4:-9,:-6])
	f1_ax2.plot(range(0,len(data_y[-48:])), data_y[-48:], 'o-', color='slateblue', lw=0.2, ms=2)
	f1_ax2.set_title("last 48 imgs")
	f1_ax2.set_ylabel('defocus [um]')
	f1_ax2.hlines(max(data_y[-48:]), 0, len(data_x[-48:]), colors='blue', linestyles='dotted', label='max')
	f1_ax2.hlines(min(data_y[-48:]), 0, len(data_x[-48:]), colors='red', linestyles='dotted', label='min')
	f1_ax2.hlines(np.mean(data_y[-48:]), 0, len(data_x[-48:]), colors='dimgray', linestyles='dashed', label='avg')
	###numpy array derived from the ctf image displayed with imshow:second last image###
	#if len(avg_defocus) > 200 :	
	#f1_ax3 = fig.add_subplot(spec[4:-9,2:-4])
	f1_ax3.plot(range(0,len(data_y[-32:])), data_y[-32:], 'o-', color='slateblue', lw=0.2, ms=2)
	f1_ax3.set_title("last 32 imgs")
	#f1_ax3.set_ylabel('defocus [um]')
	f1_ax3.hlines(max(data_y[-32:]), 0, len(data_x[-32:]), colors='blue', linestyles='dotted', label='max')
	f1_ax3.hlines(min(data_y[-32:]), 0, len(data_x[-32:]), colors='red', linestyles='dotted', label='min')
	f1_ax3.hlines(np.mean(data_y[-32:]), 0, len(data_x[-32:]), colors='dimgray', linestyles='dashed', label='avg')	
	#plt.hist(data_y[pc20_data_y:], bins=20, range=(0,3), density=True, color='slateblue')
	#f1_ax3.set_title("last 20% imgs")
	#f1_ax3.set_xlabel('defocus [um]')
	#f1_ax3 = fig.add_subplot(spec[5:-4,2:-2])
	#if len(avg_defocus) > 100 :	
	#f1_ax7 = fig.add_subplot(spec[4:-9,4:-2])
	f1_ax7.plot(range(0,len(data_y[-16:])), data_y[-16:], 'o-', color='slateblue', lw=0.2, ms=2)
	f1_ax7.set_title("last 16 imgs")
	f1_ax7.hlines(max(data_y[-16:]), 0, len(data_x[-16:]), colors='blue', linestyles='dotted', label='max')
	f1_ax7.hlines(min(data_y[-16:]), 0, len(data_x[-16:]), colors='red', linestyles='dotted', label='min')
	f1_ax7.hlines(np.mean(data_y[-16:]), 0, len(data_x[-16:]), colors='dimgray', linestyles='dashed', label='avg')
	#plt.hist(data_y[pc10_data_y:], bins=20, range=(0,3), density=True, color='slateblue')
	#f1_ax7.set_title("last 10% imgs")	
	#f1_ax7.set_xlabel('defocus [um]')
	###
	###numpy array derived from the ctf image displayed with imshow:second last image###
	#f1_ax7 = fig.add_subplot(spec[5:-4,4:])
	#plt.imshow(ctf_np_512_3, cmap='binary')
	#f1_ax7.set_xticks([])
	#f1_ax7.set_yticks([])
	#f1_ax7.set_title("third last image")
	###plot resolution data with horizontal lines for max, min,avg resolution###
	f1_ax4.plot(data_x2, data_y2, 'o-', color='darkorange', lw=0.2, ms=2)
	f1_ax4.set_ylim([2,6])
	f1_ax4.set_ylabel('resolution [A]')
	f1_ax4.set_title('image number all', y=1)
	f1_ax4.hlines(max(data_y2), 0, len(data_x2), colors='blue', linestyles='dotted')
	f1_ax4.hlines(min(data_y2), 0, len(data_x2), colors='red', linestyles='dotted')
	f1_ax4.hlines(np.mean(data_y2), 0, len(data_x2), colors='black', linestyles='dashed')
	
	###plot defocus histogram ###
	f1_ax5.hist(data_y, bins=20, range=(0,3), density=True, color='slateblue')
	#f1_ax5.set_xlabel('defocus [um]')
	#f1_ax5.tick_params(bottom=False, top=True, labelbottom=False, labeltop=True)
	f1_ax5.set_title('defocus histogram all', y=1)
	###plot resolution histogram###
	f1_ax6.hist(data_y2, bins=20, range=(3,5), density=True, color='darkorange')
	#f1_ax6.set_xlabel('resolution')
	#f1_ax5.tick_params(bottom=False, top=True, labelbottom=False, labeltop=True)
	f1_ax6.set_title('resolution histogram all', y=1)

	###numpy array derived from the ctf image displayed with imshow:last image###
	#if len(avg_defocus) > 300:	
	f1_ax8.plot(range(0,len(data_y2[-48:])), data_y2[-48:], 'o-', color='darkorange', lw=0.2, ms=2)
	f1_ax8.set_title("last 48 imgs")
	f1_ax8.set_ylabel('resolution [A]')
	f1_ax8.set_ylim([2,6])
	f1_ax8.hlines(max(data_y2[-48:]), 0, len(data_x2[-48:]), colors='blue', linestyles='dotted', label='max')
	f1_ax8.hlines(min(data_y2[-48:]), 0, len(data_x2[-48:]), colors='red', linestyles='dotted', label='min')
	f1_ax8.hlines(np.mean(data_y2[-48:]), 0, len(data_x2[-48:]), colors='dimgray', linestyles='dashed', label='avg')	
	#f1_ax8 = fig.add_subplot(spec[12:-1,:-6])
	#f1_ax8.hist(data_y2[pc30_data_y2:], bins=20, range=(1,6), density=True, color='darkorange')
	#f1_ax8.set_title("last 30% imgs")
	#f1_ax8.set_xlabel('resolution [A]')
	###numpy array derived from the ctf image displayed with imshow:second last image###
	#if len(avg_defocus) > 200 :	
	f1_ax9.plot(range(0,len(data_y2[-32:])), data_y2[-32:], 'o-', color='darkorange', lw=0.2, ms=2)
	f1_ax9.set_title("last 32 imgs")
	f1_ax9.set_ylim([2,6])
	f1_ax9.hlines(max(data_y2[-32:]), 0, len(data_x2[-32:]), colors='blue', linestyles='dotted', label='max')
	f1_ax9.hlines(min(data_y2[-32:]), 0, len(data_x2[-32:]), colors='red', linestyles='dotted', label='min')
	f1_ax9.hlines(np.mean(data_y2[-32:]), 0, len(data_x2[-32:]), colors='dimgray', linestyles='dashed', label='avg')
	#f1_ax9 = fig.add_subplot(spec[12:-1,2:-4])
	#f1_ax9.hist(data_y2[pc20_data_y2:], bins=20, range=(1,6), density=True, color='darkorange')
	#f1_ax9.set_title("last 20% imgs")
	#f1_ax9.set_xlabel('resolution [A]')
	#f1_ax3 = fig.add_subplot(spec[5:-4,2:-2])
	#if len(avg_defocus) > 100 :	
	f1_ax10.plot(range(0,len(data_y2[-16:])), data_y2[-16:], 'o-', color='darkorange', lw=0.2, ms=2)
	f1_ax10.set_title("last 16 imgs")
	f1_ax10.set_ylim([2,6])
	f1_ax10.hlines(max(data_y2[-16:]), 0, len(data_x2[-16:]), colors='blue', linestyles='dotted', label='max')
	f1_ax10.hlines(min(data_y2[-16:]), 0, len(data_x2[-16:]), colors='red', linestyles='dotted', label='min')
	f1_ax10.hlines(np.mean(data_y2[-16:]), 0, len(data_x2[-16:]), colors='dimgray', linestyles='dashed', label='avg')
	#f1_ax10 = fig.add_subplot(spec[12:-1,4:-2])
	#f1_ax10.hist(data_y2[pc20_data_y2:], bins=20, range=(1,6), density=True, color='darkorange')
	#f1_ax10.set_title("last 10% imgs")	
	#f1_ax10.set_xlabel('resolution [A]')
	#polar azymuth_all
	if len(data_y3) == len(data_x3):
		f1_ax11.scatter(data_y3, data_x3, c='limegreen', s=1, alpha=0.75)
		f1_ax11.set_title('Azymuth all', y=1)
		#if len(azymuth_list) > 100 :	
		f1_ax12.scatter(data_y3[pc10_data_y3:], data_x3[pc10_data_x3:], c='limegreen', s=1, alpha=0.75)
		f1_ax12.set_xlabel('last 10% imgs')
		#if len(azymuth_list) > 200 :	
		f1_ax13.scatter(data_y3[pc20_data_y3:], data_x3[pc20_data_x3:], c='limegreen', s=1, alpha=0.75)
		f1_ax13.set_xlabel('azymuth last 20% imgs')
		#if len(azymuth_list) > 300 :	
		f1_ax14.scatter(data_y3[pc30_data_y3:], data_x3[pc30_data_x3:], c='limegreen', s=1, alpha=0.75)
		f1_ax14.set_xlabel('azymuth last 30% imgs')		
ani = animation.FuncAnimation(fig, animate, fargs=(data_x, data_y, data_x2, data_y2), interval=3000)
plt.show()
#	avg_defocus = []
	#time.sleep(2)
