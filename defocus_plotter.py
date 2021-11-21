import os
import sys
import time
import matplotlib.pyplot as plt
import statistics
import pickle
import matplotlib.animation as animation
###using animation func reading a list of defocus values from a pkl file###
fig, ax = plt.subplots()
data_x = []
data_y = []
def animate(i, data_x, data_y):
	with open('avg_defocus.pkl', 'rb') as f:
		avg_defocus = pickle.load(f)	
	data_x = range(0, len(avg_defocus))
	data_y = avg_defocus
	# Draw x and y lists
	ax.clear()
	ax.plot(data_x, data_y, 'go-')
ani = animation.FuncAnimation(fig, animate, fargs=(data_x, data_y), interval=500)
plt.show()
