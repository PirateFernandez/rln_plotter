import os
import sys
import time
import matplotlib.pyplot as plt
import statistics
import pickle
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec
import numpy as np
import mrcfile
fig = plt.figure(figsize=(15,15))
spec = gridspec.GridSpec(ncols=8, nrows=30 , wspace=2)
subspec1 = gridspec.GridSpecFromSubplotSpec(10, 40,subplot_spec=spec[18:,0:-2], wspace=-0.2, hspace=-0.9)
subspec2 = gridspec.GridSpecFromSubplotSpec(24, 1,subplot_spec=spec[20:,6:], wspace=-0.5, hspace=0.0)
      
#row1
f1_ax1 = fig.add_subplot(spec[0:4,0:4])
f1_ax2 = fig.add_subplot(spec[0:4,4:6])
f1_ax3 = fig.add_subplot(spec[0:4,6:], projection='polar')
#row2
f1_ax4 = fig.add_subplot(spec[5:9,0:2])
f1_ax5 = fig.add_subplot(spec[5:9,2:4])
f1_ax6 = fig.add_subplot(spec[5:9,4:6])
f1_ax7 = fig.add_subplot(spec[5:9,6:], projection='polar')
f1_ax7.set_yticklabels([])
#row3
f1_ax8 = fig.add_subplot(spec[10:14,0:4])
f1_ax9 = fig.add_subplot(spec[10:14,4:6])
f1_ax10 = fig.add_subplot(spec[10:14,6:], projection='polar')
f1_ax10.set_yticklabels([])
#row4
f1_ax11 = fig.add_subplot(spec[15:19,0:2])
f1_ax12 = fig.add_subplot(spec[15:19,2:4])
f1_ax13 = fig.add_subplot(spec[15:19,4:6])
f1_ax14 = fig.add_subplot(spec[15:19,6:], projection='polar')
f1_ax14.set_yticklabels([])
#row5
f1_ax15 = fig.add_subplot(spec[20:21,0:6])
f1_ax15.set_yticklabels([])
f1_ax15.set_xticklabels([])
f1_ax15.set_xticks([])
f1_ax15.set_yticks([])
#text-box
f1_ax16 = fig.add_subplot(subspec2[0:,0:])
f1_ax16.set_yticklabels([])
f1_ax16.set_xticklabels([])
f1_ax16.set_xticks([])
f1_ax16.set_yticks([])
#row6
#f1_ax17 = fig.add_subplot(spec[25:29,0:4])
#f1_ax18 = fig.add_subplot(spec[25:29,4:])
#f1_ax14.set_yticklabels([])
###define data to be reprsented and pass to animation function###
data_x = []
data_y = []
data_x2 = []
data_y2 = []
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
	###preparing data for plotting###
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
	###dummy data###
	data_xk = [i for i in range(100)]
	data_yk = [i*i for i in range(100)]
	#Clean defocus plot before re-ploting###
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
	f1_ax11.clear()
	f1_ax12.clear()
	f1_ax13.clear()
	f1_ax14.clear()
	f1_ax15.clear()
	f1_ax16.clear()
	#f1_ax17.clear()
	#f1_ax18.clear()
	#plotting row 1
		#ax1->plot all defoci vs image number
	f1_ax1.plot(data_x, data_y, 'o-', color='slateblue', lw=0.2, ms=2)
	f1_ax1.set_ylabel('defocus [um]')
	f1_ax1.set_ylim([0,6])
	f1_ax1.tick_params(bottom=True, top=False, labelbottom=True, labeltop=False)
	f1_ax1.set_title('image number all', y=1)
	f1_ax1.hlines(max(data_y), 0, len(data_x), colors='blue', linestyles='dotted', label='max')
	f1_ax1.hlines(min(data_y), 0, len(data_x), colors='red', linestyles='dotted', label='min')
	f1_ax1.hlines(np.mean(data_y), 0, len(data_x), colors='dimgray', linestyles='dashed', label='avg')
		#ax2->hist all defoci vs image number
	f1_ax2.hist(data_y, bins=20, range=(0,10), density=True, color='slateblue')
	f1_ax2.set_title('defocus histogram all', y=1)
		#ax3->polar all astigmatism	
	f1_ax3.scatter(data_y3, data_x3, c='limegreen', s=1, alpha=0.75)
	f1_ax3.set_title('Azymuth all', y=1)
	f1_ax3.set_xticklabels([])
	#plotting row 2
		#ax4->plot last 48 defocus vs image number
	f1_ax4.plot(range(0,len(data_y[-48:])), data_y[-48:], 'o-', color='slateblue', lw=0.2, ms=2)
	f1_ax4.set_title("last 48 imgs")
	f1_ax4.set_ylabel('defocus [um]')
	f1_ax4.hlines(max(data_y[-48:]), 0, len(data_x[-48:]), colors='blue', linestyles='dotted', label='max')
	f1_ax4.hlines(min(data_y[-48:]), 0, len(data_x[-48:]), colors='red', linestyles='dotted', label='min')
	f1_ax4.hlines(np.mean(data_y[-48:]), 0, len(data_x[-48:]), colors='dimgray', linestyles='dashed', label='avg')
	f1_ax4.set_ylim([0,6])
		#ax5->plot last 32 defocus vs image number	
	f1_ax5.plot(range(0,len(data_y[-32:])), data_y[-32:], 'o-', color='slateblue', lw=0.2, ms=2)
	f1_ax5.set_title("last 32 imgs")
	f1_ax5.set_ylabel('defocus [um]')
	f1_ax5.hlines(max(data_y[-32:]), 0, len(data_x[-32:]), colors='blue', linestyles='dotted', label='max')
	f1_ax5.hlines(min(data_y[-32:]), 0, len(data_x[-32:]), colors='red', linestyles='dotted', label='min')
	f1_ax5.hlines(np.mean(data_y[-32:]), 0, len(data_x[-32:]), colors='dimgray', linestyles='dashed', label='avg')
	f1_ax5.set_ylim([0,6])
		#ax6->plot last 16 defoci vs image number	
	f1_ax6.plot(range(0,len(data_y[-16:])), data_y[-16:], 'o-', color='slateblue', lw=0.2, ms=2)
	f1_ax6.set_title("last 16 imgs")
	f1_ax6.set_ylabel('defocus [um]')
	f1_ax6.hlines(max(data_y[-16:]), 0, len(data_x[-16:]), colors='blue', linestyles='dotted', label='max')
	f1_ax6.hlines(min(data_y[-16:]), 0, len(data_x[-16:]), colors='red', linestyles='dotted', label='min')
	f1_ax6.hlines(np.mean(data_y[-16:]), 0, len(data_x[-16:]), colors='dimgray', linestyles='dashed', label='avg')
	f1_ax6.set_ylim([0,6])
		#ax7->polar 30% images astisgmatism	
	f1_ax7.scatter(data_y3[pc30_data_y3:], data_x3[pc30_data_x3:], c='limegreen', s=1, alpha=0.75)
	f1_ax7.set_title('Azymuth last 30% data', y=1)
	f1_ax7.set_xticklabels([])
	#plotting row 3
		#ax8->plot all res vs image number
	f1_ax8.plot(data_x2, data_y2, 'o-', color='darkorange', lw=0.2, ms=2)
	f1_ax8.set_ylim([2,8])
	f1_ax8.set_ylabel('resolution [A]')
	f1_ax8.set_title('image number all', y=1)
	f1_ax8.hlines(max(data_y2), 0, len(data_x2), colors='blue', linestyles='dotted')
	f1_ax8.hlines(min(data_y2), 0, len(data_x2), colors='red', linestyles='dotted')
	f1_ax8.hlines(np.mean(data_y2), 0, len(data_x2), colors='black', linestyles='dashed')
		#ax9->hist all res	
	f1_ax9.hist(data_y2, bins=20, range=(0,10), density=True, color='darkorange')
	f1_ax9.set_title('resolution histogram all', y=1)
		#ax10->polar 20% images astismagtim	
	f1_ax10.scatter(data_y3[pc20_data_y3:], data_x3[pc20_data_x3:], c='limegreen', s=1, alpha=0.75)
	f1_ax10.set_title('Azymuth last 20% data', y=1)
	f1_ax10.set_xticklabels([])
	#plotting row 4
		#ax11->plot res last 48 images vs image number
	f1_ax11.plot(range(0, len(data_y2[-48:])), data_y2[-48:], 'o-', color='darkorange', lw=0.2, ms=2)
	f1_ax11.set_title("last 48 imgs")
	f1_ax11.set_ylabel('resolution [A]')
	f1_ax11.set_ylim([2,8])
	f1_ax11.hlines(max(data_y2[-48:]), 0, len(data_x2[-48:]), colors='blue', linestyles='dotted', label='max')
	f1_ax11.hlines(min(data_y2[-48:]), 0, len(data_x2[-48:]), colors='red', linestyles='dotted', label='min')
	f1_ax11.hlines(np.mean(data_y2[-48:]), 0, len(data_x2[-48:]), colors='dimgray', linestyles='dashed', label='avg')
		#ax12->plot res last 32 images vs image number	
	f1_ax12.plot(range(0, len(data_y2[-32:])), data_y2[-32:], 'o-', color='darkorange', lw=0.2, ms=2)
	f1_ax12.set_title("last 32 imgs")
	f1_ax12.set_ylabel('resolution [A]')
	f1_ax12.set_ylim([2,8])
	f1_ax12.hlines(max(data_y2[-32:]), 0, len(data_x2[-32:]), colors='blue', linestyles='dotted', label='max')
	f1_ax12.hlines(min(data_y2[-32:]), 0, len(data_x2[-32:]), colors='red', linestyles='dotted', label='min')
	f1_ax12.hlines(np.mean(data_y2[-32:]), 0, len(data_x2[-32:]), colors='dimgray', linestyles='dashed', label='avg')
		#ax13->plot res last 16 images vs image number	
	f1_ax13.plot(range(0,len(data_y2[-16:])), data_y2[-16:], 'o-', color='darkorange', lw=0.2, ms=2)
	f1_ax13.set_title("last 16 imgs")
	f1_ax13.set_ylabel('resolution [A]')
	f1_ax13.set_ylim([2,8])
	f1_ax13.hlines(max(data_y2[-16:]), 0, len(data_x2[-16:]), colors='blue', linestyles='dotted', label='max')
	f1_ax13.hlines(min(data_y2[-16:]), 0, len(data_x2[-16:]), colors='red', linestyles='dotted', label='min')
	f1_ax13.hlines(np.mean(data_y2[-16:]), 0, len(data_x2[-16:]), colors='dimgray', linestyles='dashed', label='avg')
		#ax14->polar 10% images astismatism	
	f1_ax14.scatter(data_y3[pc10_data_y3:], data_x3[pc10_data_x3:], c='limegreen', s=1, alpha=0.75)
	f1_ax14.set_title('Azymuth last 10% data', y=1)
	f1_ax14.set_xticklabels([])
	
	####dataset statisticks
	#total_num_images = len(avg_defocus)
	f1_ax16.set_xticks([])
	f1_ax16.set_yticks([])
	f1_ax16.text(0.25,0.94, f"Imgs corrected:", fontweight='bold')
	f1_ax16.text(0.38,0.88, f"{len(avg_defocus)}", color='red')
	def_belw_1u = [def_1 for def_1 in avg_defocus if def_1 < 1 ]
	f1_ax16.text(0.04,0.8, f"Imgs def <-1uM: ", fontweight='bold')
	f1_ax16.text(0.32,0.75, f"{len(def_belw_1u)} ({round((len(def_belw_1u)*100)/len(avg_defocus),2)}%)")
	def_belw_2u = [def_1 for def_1 in avg_defocus if def_1 < 2 and def_1 >1 ]
	f1_ax16.text(0.04,0.7, f"Imgs def >-1 and <-2uM:", fontweight='bold')
	f1_ax16.text(0.32,0.65, f"{len(def_belw_2u)} ({round((len(def_belw_2u)*100)/len(avg_defocus),2)}%)")
	def_belw_3u = [def_1 for def_1 in avg_defocus if def_1 < 3 and def_1 >2 ]
	f1_ax16.text(0.04,0.60, f"Imgs def >2 and <-3uM:", fontweight='bold')
	f1_ax16.text(0.32,0.55, f"{len(def_belw_3u)} ({round((len(def_belw_3u)*100)/len(avg_defocus),2)}%)")
	###
	res_belw_2A = [res_1 for res_1 in resolution_list_local if res_1 < 2 ]
	res_belw_3A = [res_1 for res_1 in resolution_list_local if res_1 > 2 and res_1 < 3  ]
	res_belw_4A = [res_1 for res_1 in resolution_list_local if res_1 > 3 and res_1 < 4 ]
	res_belw_5A = [res_1 for res_1 in resolution_list_local if res_1 > 4 ]
	f1_ax16.text(0.04,0.43, f"Imgs res < 2A: ", fontweight='bold')
	f1_ax16.text(0.32,0.38, f"{len(res_belw_2A)} ({round((len(res_belw_2A)*100)/len(resolution_list_local),2)}%)")
	def_belw_2u = [def_1 for def_1 in avg_defocus if def_1 < 2 and def_1 >1 ]
	f1_ax16.text(0.04,0.33, f"Imgs res >2 and < 3A:", fontweight='bold')
	f1_ax16.text(0.32,0.28, f"{len(res_belw_3A)} ({round((len(res_belw_3A)*100)/len(resolution_list_local),2)}%)")
	def_belw_3u = [def_1 for def_1 in avg_defocus if def_1 < 3 and def_1 >2 ]
	f1_ax16.text(0.04,0.23, f"Imgs res > 3 and < 4A:", fontweight='bold')
	f1_ax16.text(0.32,0.18, f"{len(res_belw_4A)} ({round((len(res_belw_4A)*100)/len(resolution_list_local),2)}%)")
	f1_ax16.text(0.04,0.13, f"Imgs res >4A:", fontweight='bold')
	f1_ax16.text(0.32,0.08, f"{len(res_belw_5A)} ({round((len(res_belw_5A)*100)/len(resolution_list_local),2)}%)")
	
	####capture all jobs folders.###
	rln_directory = os.getcwd()
	checking_dir = f"{rln_directory}/Class2D"	
	if os.path.isdir(checking_dir) :
		select_elements = os.listdir(f'{rln_directory}/Class2D')
		select_jobs = []
		for i in select_elements:
			if 'job' in i:
				select_jobs.append(i)
		###identify the highest job number to look for run_it200_classes.mrcs ###
		jobs_numbers = []
		for i in select_jobs:
			i_split = i.split("b")
			jobs_numbers.append(int(i_split[-1]))
			
		if max(jobs_numbers) > 99:
			lastest_job = f"job{max(jobs_numbers)}"
			#print(lastest_job)
		elif max(jobs_numbers) < 100  and max(jobs_numbers) > 9:
			lastest_job = f"job0{max(jobs_numbers)}"
		elif max(jobs_numbers) < 10:
			lastest_job = f"job00{max(jobs_numbers)}"
			#print(lastest_job)
		###
		jobs_numbers_sorted = sorted(jobs_numbers)
		jobs_sorted = []
		for i in jobs_numbers_sorted:
			if i < 10:
				jobs_sorted.append(f"job00{i}")
			elif i > 10 and i < 100:
				jobs_sorted.append(f"job0{i}")
			elif i > 99:
				jobs_sorted.append(f"job{i}")
		#print(f"{lastest_job}")
		###load it200.mrcs from the highest job number.###
		path_to_last = f"{rln_directory}/Class2D/{lastest_job}/run_it200_classes.mrcs"
		path_to_last_strip = path_to_last.strip()
		#print(f"{path_to_last_strip}")		
		if os.path.isfile(path_to_last):	
			c2d_file = f"{rln_directory}/Class2D/{lastest_job}/run_it200_classes.mrcs"
			print(f"{path_to_last}")	
			with mrcfile.open(c2d_file) as emd:
				nx, ny, nz = emd.header['nx'], emd.header['ny'], emd.header['nz']
				c2d_flat = emd.data.flatten(order='F').reshape(emd.header['nx'], emd.header['ny'], emd.header['nz'])
			row_inx = []
			for i in range(0,10,2):
				for j in range(0,20):
					row_inx.append(i)
			col_inx = []
			for j in range(10):
				for i in range(0,40,2):
					col_inx.append(i)
			for ri, ci, i in zip(row_inx, col_inx, range(0,100)):
				ax = fig.add_subplot(subspec1[ri:ri+2, ci:ci+2])
				ax.imshow(c2d_flat[:,:,i], cmap='gray')
				ax.set_xticks([])
				ax.set_yticks([])
			###for c2d label
			f1_ax15.text(0.425,0.4, f"C2D-{lastest_job}",fontweight='bold', fontsize='large')
			f1_ax15.set_yticklabels([])
			f1_ax15.set_xticklabels([])
			f1_ax15.set_xticks([])
			f1_ax15.set_yticks([])
		elif len(jobs_sorted) >= 3 :
			c2d_file = f"{rln_directory}/Class2D/{jobs_sorted[-2]}/run_it200_classes.mrcs"
			print(f"{c2d_file}")

			with mrcfile.open(c2d_file) as emd:
				nx, ny, nz = emd.header['nx'], emd.header['ny'], emd.header['nz']
				c2d_flat = emd.data.flatten(order='F').reshape(emd.header['nx'], emd.header['ny'], emd.header['nz'])
			row_inx = []
			for i in range(0,10,2):
				for j in range(0,20):
					row_inx.append(i)
			col_inx = []
			for j in range(10):
				for i in range(0,40,2):
					col_inx.append(i)

			for ri, ci, i in zip(row_inx, col_inx, range(0,100)):
				ax = fig.add_subplot(subspec1[ri:ri+2, ci:ci+2])
				ax.imshow(c2d_flat[:,:,i], cmap='gray')
				ax.set_xticks([])
				ax.set_yticks([])
			###for c2d label
			f1_ax15.text(0.425,0.4, f"C2D-{jobs_sorted[-2]}", fontweight='bold', fontsize='large')
			f1_ax15.set_yticklabels([])
			f1_ax15.set_xticklabels([])
			f1_ax15.set_xticks([])
			f1_ax15.set_yticks([])
				#
		elif  len(jobs_sorted) == 2 :
			c2d_file = f"{rln_directory}/Class2D/{jobs_sorted[0]}/run_it200_classes.mrcs"
			print(f"{c2d_file}")

			with mrcfile.open(c2d_file) as emd:
				nx, ny, nz = emd.header['nx'], emd.header['ny'], emd.header['nz']
				c2d_flat = emd.data.flatten(order='F').reshape(emd.header['nx'], emd.header['ny'], emd.header['nz'])
			row_inx = []
			for i in range(0,10,2):
				for j in range(0,20):
					row_inx.append(i)
			col_inx = []
			for j in range(10):
				for i in range(0,40,2):
					col_inx.append(i)

			for ri, ci, i in zip(row_inx, col_inx, range(0,100)):
				ax = fig.add_subplot(subspec1[ri:ri+2, ci:ci+2])
				ax.imshow(c2d_flat[:,:,i], cmap='gray')
				ax.set_xticks([])
				ax.set_yticks([])
			f1_ax15.text(0.425,0.4, f"C2D-{jobs_sorted[0]}",fontweight='bold', fontsize='large')
			f1_ax15.set_yticklabels([])
			f1_ax15.set_xticklabels([])
			f1_ax15.set_xticks([])
			f1_ax15.set_yticks([])
	else :
		f1_ax15.text(0.425,0.4, f"NO C2D YET",fontweight='bold', fontsize='large')
		f1_ax15.set_yticklabels([])
		f1_ax15.set_xticklabels([])
		f1_ax15.set_xticks([])
		f1_ax15.set_yticks([])
		
				#
ani = animation.FuncAnimation(fig, animate, fargs=(data_x, data_y, data_x2, data_y2), interval=10000)
plt.show()	
