import os
import sys
import time
import statistics
import pickle
""" check if the user supplied path to ctffind log files, if not handle the exception."""
try:
	filepath_ctffind4 = sys.argv[1]
except IndexError:
	print("### Wrong usage, please provide path to ctffind.log folder###")
	print("Correct usage:")
	print("############################################################")
	print("pythonn3.x defocus_catcher.py path_to_ctffind_log_files_folder")
	print("############################################################")
	print("### Please provide path to origin folder###")
	exit()
while True:	
	###get list of all files in the directory supplied###
	file_list_all = os.listdir(filepath_ctffind4)
	###initialize lists where to store files names, file names with path for the .log files###
	file_list_ctffind4_log = []
	file_list_ctffind_4_log_with_path = []
	###initialize lists where to store files names, file names with path for the .ctf files###
	file_list_ctffind_4_PS = []
	file_list_ctffind_4_PS_with_path = []
	"""loop to populate lists with only ctffind4.log files (list_2)"""
	for i in file_list_all:
		if 'ctffind4.log' in i:
			file_list_ctffind4_log.append(i)
	"""loop to populate list path+ctffind4.log (list_3)"""
	for i in file_list_ctffind4_log:
		file_list_ctffind_4_log_with_path.append(f"{filepath_ctffind4}/{i}")	
	"""loop to populate lists with only ctffind4_PS.ctf files (list_2)"""
	#for i in file_list_all:
	#	if 'PS.ctf' in i:
	#		file_list_ctffind_4_PS.append(i)
	"""loop to populate list path+ctffind4_PS.ctf (list_3)"""
	#for i in file_list_ctffind_4_PS:
	#	file_list_ctffind_4_PS_with_path.append(f"{filepath_ctffind4}/{i}")
 	###sort lists of files by ascending time of creation, last file created, last file in the lest###
	file_list_ctffind_4_log_with_path_sorted = sorted(file_list_ctffind_4_log_with_path, key=lambda t: os.stat(t).st_mtime)

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
	def extract_resolution(filelistwithpath):
		resolution_1 = []
		defocus_1_um = []
		for i in filelistwithpath:
			with open(i, 'r') as f:
				f_lines = f.readlines()
				for i2 in f_lines:
					if 'Thon rings with good fit up to  :' in i2:
						i2_split = i2.split(" ")
						defocus_1.append(float(i2_split[11]))
		defocus_1_um = [i/10000 for i in defocus_1]
		return defocus_1_um
	def extract_resolution(file_1):
		resolution_1 = []
		for i in file_1:
			with open(i, 'r') as f:
				f_lines = f.readlines()
				for i2 in f_lines:
					if 'Thon rings with good fit up to  :' in i2:
						i2_split = i2.split(" ")
						resolution_1.append(float(i2_split[9]))
		return resolution_1
	def extract_azymuth(filelistwithpath):
		azymuth_1 = []
		for i in filelistwithpath:
			with open(i, 'r') as f:
				f_lines = f.readlines()
				for i2 in f_lines:
					if 'Estimated azimuth of astigmatism:' in i2:
						i2_split = i2.split(" ")
						azymuth_1.append(float(i2_split[-2]))
		return azymuth_1	
	def delta_defoc(listdefocus1, listdefocus2):
		delta_defocus_1 = []
		for  i, i2 in zip(listdefocus1, listdefocus2):
			dif = round(abs((i -i2)), 2)
			delta_defocus_1.append(dif)
		return 	delta_defocus_1		
	###
	list_defocus_1 = extract_defocus_1(file_list_ctffind_4_log_with_path_sorted)
	list_defocus_2 = extract_defocus_2(file_list_ctffind_4_log_with_path_sorted)
	avg_defocus_glob = avg_defocus(list_defocus_1, list_defocus_2)
	avg_defocus_glob_2f = []
	resolution_list = extract_resolution(file_list_ctffind_4_log_with_path_sorted)
	list_azymuth = extract_azymuth(file_list_ctffind_4_log_with_path_sorted)
	list_defocus_dif = delta_defoc(list_defocus_1, list_defocus_2)
	#reduce significant numbers to two###
	for i in avg_defocus_glob:
		i2 = float(f"{i:.2f}")
		avg_defocus_glob_2f.append(i2)
	###write up pkl files with list for defocus_plotter###
	with open('avg_defocus.pkl', 'wb') as f:
		pickle.dump(avg_defocus_glob_2f, f)
	#with open('PS_ctf_files.pkl', 'wb') as f:
	#	pickle.dump(file_list_ctffind_4_PS_with_path, f)
	with open('resolution_list.pkl', 'wb') as f:
		pickle.dump(resolution_list, f)
	with open('azymuth.pkl', 'wb') as f:
		pickle.dump(list_azymuth, f)
	with open('defocus_dif.pkl', 'wb') as f:
		pickle.dump(list_defocus_dif, f)
	print(f"{list_defocus_dif[-10:]}")

	time.sleep(2)
