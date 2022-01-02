###python script to visualize rln4 c2d files automaticaly selected. Rln4 crates a images.npy file which ia numpy array with 3 dimensions.###
###The first dimension is the number of c2d, the second and thrid dimensions are the images themselves as numpy array.###
### One exaple [24,64,64]-> 24 classes with 64x64 pixel dimensions.####
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
###first we load the nmpu array stored as .npy file in an object.###
np_images_loaded =  np.load('/Users/israel_CUMC/Documents/python_work/numpy_files_rln4/images.npy')
###the size of the first dimension is the number of c2d selected.###
number_of_c2ds = np.size(np_images_loaded, 0)
x_dim = np.size(np_images_loaded, 1)
y_dim = np.size(np_images_loaded, 2)
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
