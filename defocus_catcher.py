import os
import sys
import time
import matplotlib.pyplot as plt
import statistics
import pickle
###loop catching ctf values from the ctffind.log files and dumping them into a pkl file###
""" check if the user supplied path to motioncor log files, if not handle the exception."""
while True:	
	#try:
	#	filepath_ctffind4 = sys.argv[1]
	#except IndexError:
	#	print("Wrong usage, please input desired resolution limit.")
	#	print("Correct usage:")
	#	print("pythonn3.x ctfind4_sort_by_res.py /path/path/relion_dir/CtfFind/jobxxx/yyy res_limit")
	#	print("Please provide a resolution limit.")
	#	exit()
	filepath_ctffind4 ='/home/iferna49/programs/scripts/ctfind_2'
	###
	file_list_all = os.listdir(filepath_ctffind4)
	file_list_ctffind4_log = []
	file_list_ctffind_4_log_with_path = []
	"""loop to generate lists with only ctffind4.log files (list_2)"""
	for i in file_list_all:
		if 'ctffind4.log' in i:
			file_list_ctffind4_log.append(i)
	"""loop to generate list path+ctffind4.log (list_3)"""
	for i in file_list_ctffind4_log:
		file_list_ctffind_4_log_with_path.append(f"{filepath_ctffind4}/{i}")	


	###functions to operated in log files###
	def extract_defocus_1(filelistwithpath):
		defocus_1 = []
		defocus_1_um = []
		for i in filelistwithpath:
			with open(i, 'r') as f:
				f_lines = f.readlines()
				for i2 in f_lines:
					if 'Estimated defocus values        :' in i2:
						i2_split = i2.split(" ")
						defocus_1.append(float(i2_split[11]))
		defocus_1_um = [i/10000 for i in defocus_1]
		return defocus_1_um

	def extract_defocus_2(filelistwithpath):
		defocus_2 = []
		defocus_2_um = []
		for i in filelistwithpath:
			with open(i, 'r') as f:
				f_lines = f.readlines()
				for i2 in f_lines:
					if 'Estimated defocus values        :' in i2:
						i2_split = i2.split(" ")
						defocus_2.append(float(i2_split[13]))
		defocus_2_um = [i/10000 for i in defocus_2]
		return defocus_2_um

	def avg_defocus(listdefocus1, listdefocus2):
		avg_defocus_list = []
		for i in range(0, len(listdefocus1)):
			i_avg = (listdefocus1[i]+listdefocus2[i])/2
			avg_defocus_list.append(i_avg)
		return avg_defocus_list
	###
	list_defocus_1 = extract_defocus_1(file_list_ctffind_4_log_with_path)
	list_defocus_2 = extract_defocus_2(file_list_ctffind_4_log_with_path)
	avg_defocus_glob = avg_defocus(list_defocus_1, list_defocus_2)
	avg_defocus_glob_2f = []
	#
	for i in avg_defocus_glob:
		i2 = float(f"{i:.2f}")
		avg_defocus_glob_2f.append(i2)
	x_defocus_1 = [ i for i in range(1,(len(list_defocus_1)+1))]
	x_defocus_2 = [ i for i in range(1,(len(list_defocus_2)+1))]
	x_defocus_avg = [ i for i in range(1,(len(avg_defocus_glob_2f)+1))]

	
	last_10_avg = []
	last_10_sum = 0
	copy_avg_all = avg_defocus_glob_2f[:]
	if len(copy_avg_all) > 11: 
		while len(copy_avg_all) > 10:
			last_10 = copy_avg_all[-10:-1]
			last_10_avg.append((sum(last_10))/10)
			copy_avg_all.pop()
	with open('avg_defocus.pkl', 'wb') as f:
		pickle.dump(avg_defocus_glob_2f, f)
	print(avg_defocus_glob_2f)
	time.sleep(4)
