import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
###get rln directory path.###
rln_directory = os.getcwd()
###main condition for c2d plotting.###
if 'rln_directoy/Select' :
	###capture all jobs folders.###
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
	###load numpy array from .npy from the highest job number.###
	np_images_loaded =  np.load(f'{rln_directory}/Select/{lastest_job}/images.npy')
	###the size of the first dimension is the number of c2d selected.###
	number_of_c2ds = np.size(np_images_loaded, 0)
	###loop through the nympy array and plot with imshow###
	if (number_of_c2ds%2)==0:
		fig, axs = plt.subplots(2, int(number_of_c2ds/2), subplot_kw={'xticks': [], 'yticks': []})
		plt.subplots_adjust(wspace=0.1, hspace=-0.85)
	###ravel function to flaten the multidimensional array coming from subplots so it can be fed into the loop.###
		for i, ax in zip(range(number_of_c2ds), axs.ravel()):
			ax.imshow(np_images_loaded[i,:,:], cmap='gray')
	elif (number_of_c2ds%2)!=0:
		number_of_c2ds_even = number_of_c2ds+1
		fig, axs = plt.subplots(2, int(number_of_c2ds_even/2), subplot_kw={'xticks': [], 'yticks': []})
		plt.subplots_adjust(wspace=0.05, hspace=-0.2)
		for i, ax in zip(range(number_of_c2ds_even), axs.ravel()):
			ax.imshow(np_images_loaded[i,:,:], cmap='gray')
	plt.show()
	print(number_of_c2ds)
