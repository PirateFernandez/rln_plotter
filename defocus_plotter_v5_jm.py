import os
import sys
import time
import matplotlib.pyplot as plt
import statistics
import pickle
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec
import numpy as np


if len(sys.argv) != 2 or not os.path.exists(sys.argv[1]):
	print("### Wrong usage, please provide ctf_values.npy file to plot! ###")
	print("Correct usage:")
	print("############################################################")
	print("python defocus_plotter.py path_to_ctffind_log_files_folder/ctf_values.npy")
	print("############################################################")
	exit(1)

ctf_values_path = sys.argv[1]

print("Plotting CTF values from: ", ctf_values_path)


fig = plt.figure(figsize=(15,15))
spec = gridspec.GridSpec(ncols=8, nrows=30 , wspace=2)
subspec1 = gridspec.GridSpecFromSubplotSpec(24, 1,subplot_spec=spec[20:-1,0:4],
											wspace=0.0, hspace=0.0)
subspec2 = gridspec.GridSpecFromSubplotSpec(24, 1,subplot_spec=spec[20:-1,4:],
											wspace=0.0, hspace=0.0)
      
#row1
f1_ax1 = fig.add_subplot(spec[0:4,0:4])
f1_ax2 = fig.add_subplot(spec[0:4,4:6])
f1_ax3 = fig.add_subplot(spec[0:4,6:], projection='polar')

#row2
f1_ax4 = fig.add_subplot(spec[5:9, 0:2])
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
# f1_ax15 = fig.add_subplot(subspec1[0:-1,0:2])
# f1_ax16 = fig.add_subplot(subspec2[0:,0:])
#row6
#f1_ax17 = fig.add_subplot(spec[25:29,0:4])
#f1_ax18 = fig.add_subplot(spec[25:29,4:])
#f1_ax14.set_yticklabels([])
###define data to be reprsented and pass to animation function###
data_x = []
data_y = []
data_x2 = []
data_y2 = []


def plot_values(axis, data_y, image_number, label):
	""" Plot values for the last 'image_number' images. """
	yy = data_y[-image_number:]
	n = len(yy)
	ii = range(1, len(data_y)+1)[-image_number:]
	i = ii[0]
	axis.plot(ii, yy, 'o-', color='slateblue', lw=0.2, ms=2)
	title = "last %d images" % image_number if image_number else "all images"
	axis.set_title(title)
	axis.set_ylabel(label)
	axis.hlines(max(yy), i, i+n, colors='blue', linestyles='dotted', label='max')
	axis.hlines(min(yy), i, i+n, colors='red', linestyles='dotted', label='min')
	axis.hlines(np.mean(yy), i, i+n, colors='dimgray', linestyles='dashed', label='avg')

def plot_defocus(axis, data_y, image_number):
	""" Plot defocus values for the last 'image_number' images. """
	plot_values(axis, data_y, image_number, 'defocus [um]')

def plot_resolution(axis, data_y, image_number):
	""" Plot Resolution values for the last 'image_number' images. """
	plot_values(axis, data_y, image_number, 'resolution [A]')

def scatter(axis, data_y, percent):
	""" Make a scatter plot of a given percent of the data. """
	last_index = round((-(len(data_y) * percent) / 100))
	yy = data_y[-last_index:]
	n = len(yy)
	ii = range(0, n)
	axis.scatter(yy, ii, c='limegreen', s=1, alpha=0.75)
	axis.set_title('Azymuth last %d%% data' % percent, y=1)
	axis.set_xticklabels([])

# FIXME: Still work-in-progress
def load_latest_classes():
	""" Load latest 2d classes from the last iteration as numpy arrays. """

	return None

	####capture all jobs folders.###
	rln_directory = os.getcwd()
	np_images_loaded = None

	if 'rln_directoy/Select':
		select_elements = os.listdir(f'{rln_directory}/Select')
		select_jobs = []
		for i in select_elements:
			if 'job' in i:
				select_jobs.append(i)
		###identify the highest job number to look for images.npy###
		jobs_numbers = []
		for i in select_jobs:
			i_slpit = i.split("b")
			jobs_numbers.append(int(i_slpit[-1]))
		if max(jobs_numbers) > 99:
			lastest_job = f"job{max(jobs_numbers)}"
			#print(lastest_job)
		if max(jobs_numbers) < 100:
			lastest_job = f"job0{max(jobs_numbers)}"
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
		###load numpy array from .npy from the highest job number.###
		if os.path.isfile(f"{rln_directory}/Select/{lastest_job}/images.npy"):
			np_images_loaded =  np.load(f'{rln_directory}/Select/{lastest_job}/images.npy')
			#print(f"{rln_directory}/Select/{lastest_job}/images.npy")
		elif os.path.isfile(f"{rln_directory}/Select/{jobs_sorted[-2]}/images.npy"):
			np_images_loaded =  np.load(f'{rln_directory}/Select/{jobs_sorted[-2]}/images.npy')
		elif os.path.isfile(f"{rln_directory}/Select/{jobs_sorted[-3]}/images.npy"):
			np_images_loaded =  np.load(f'{rln_directory}/Select/{jobs_sorted[-3]}/images.npy')
		elif os.path.isfile(f"{rln_directory}/Select/{jobs_sorted[-4]}/images.npy"):
			np_images_loaded =  np.load(f'{rln_directory}/Select/{jobs_sorted[-4]}/images.npy')
		else:
			print("No c2d available.")


	return np_images_loaded

def animate(i):
	ctf_values = np.load(ctf_values_path)

	###preparing data for plotting###
	data_y = (ctf_values['defocus1'] + ctf_values['defocus2']) / 2
	data_y2 = ctf_values['resolution']
	data_x3 = abs(ctf_values['defocus1'] - ctf_values['defocus2'])
	data_y3 = ctf_values['azymuth']

	# Clean plot axis before re-plotting
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
	# f1_ax15.clear()
	# f1_ax16.clear()
	# f1_ax17.clear()
	# f1_ax18.clear()

	# plotting row 1

	# ax1->plot all defoci vs image number
	plot_defocus(f1_ax1, data_y, 0)

	# ax2->hist all defoci vs image number
	f1_ax2.hist(data_y, bins=20, range=(0,3), density=True, color='slateblue')
	f1_ax2.set_title('defocus histogram all', y=1)
	# ax3->polar all astigmatism
	f1_ax3.scatter(data_y3, data_x3, c='limegreen', s=1, alpha=0.75)
	f1_ax3.set_title('Azymuth all', y=1)
	f1_ax3.set_xticklabels([])

	#plotting row 2
	plot_defocus(f1_ax4, data_y, 48)
	plot_defocus(f1_ax5, data_y, 32)
	plot_defocus(f1_ax6, data_y, 16)

	#ax7->polar 30% images astisgmatism
	scatter(f1_ax7, data_y3, 30)

	#plotting row 3
	# ax8->plot all res vs image number
	plot_resolution(f1_ax8, data_y2, 0)

	#ax9->hist all res
	f1_ax9.hist(data_y2, bins=20, range=(0,3), density=True, color='slateblue')
	f1_ax9.set_title('defocus histogram all', y=1)

	# ax10->polar 20% images astismagtim
	scatter(f1_ax10, data_y3, 20)

	#plotting row 4
	plot_resolution(f1_ax11, data_y2, 48)
	plot_resolution(f1_ax12, data_y2, 32)
	plot_resolution(f1_ax13, data_y2, 16)

	# ax14->polar 10% images astismatism
	scatter(f1_ax14, data_y3, 10)

	# np_images = load_latest_classes()
    #
	# if np_images:
	# 	number_of_c2ds = np.size(np_images, 0)
	# 	f1_ax15.imshow(np_images[3,:,:], cmap='gray')



ani = animation.FuncAnimation(fig, animate, interval=1000)
fig.tight_layout()
plt.show()	
