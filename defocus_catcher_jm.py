import os
import sys
import time
import numpy as np


# Check than a ctffind folder is provided and it exists

if len(sys.argv) != 2 or not os.path.exists(sys.argv[1]):
	print("### Wrong usage, please provide an existing path to ctffind.log folder###")
	print("Correct usage:")
	print("############################################################")
	print("pythonn3.x defocus_catcher.py path_to_ctffind_log_files_folder")
	print("############################################################")
	print("### Please provide path to origin folder###")
	exit(1)

ctf_folder = sys.argv[1]

print("Parsing CTF values from folder: ", ctf_folder)


def defocus(parts, i):
	return float(parts[i]) / 10000

def parse_ctffind(ctffile):
	""" Extract defocus values from lines read from a ctffind log file. """
	defocus1, defocus2, resolution, azymuth = 99999, 99999, 99999, 99999
	with open(ctffile, 'r') as f:
		for line in f:
			if 'Estimated defocus values        :' in line:
				parts = line.split()
				defocus1 = defocus(parts, 4)
				defocus2 = defocus(parts, 6)
			elif 'Thon rings with good fit up to  :' in line:
				parts = line.split()
				resolution = float(parts[8])
			elif 'Estimated azimuth of astigmatism:' in line:
				parts = line.split()
				azymuth = float(parts[-2])

	return defocus1, defocus2, resolution, azymuth


def parse_gctf(ctffile):
	""" Extract defocus values from lines read from a ctffind log file. """
	defocus1, defocus2, resolution, azymuth = 99999, 99999, 99999, 99999
	with open(ctffile, 'r') as f:
		for line in f:
			if 'Final Values' in line:
				parts = line.split()
				defocus1 = defocus(parts, 0)
				defocus2 = defocus(parts, 1)
				azymuth = float(parts[2])
			elif 'Resolution limit' in line:
				parts = line.split()
				resolution = float(parts[9])

	return defocus1, defocus2, resolution, azymuth


parsed_files = []
ctf_values = []


while True:
	# List all files in the given directory
	all_files = os.listdir(ctf_folder)

	log_files = [fn for fn in all_files
				 if fn.endswith('_ctffind4.log') and fn not in parsed_files]

	###initialize lists where to store files names, file names with path for the .ctf files###
	# file_list_ctffind_4_PS = []
	# file_list_ctffind_4_PS_with_path = []
	# for i in file_list_ctffind4_log:
	# 	file_list_ctffind_4_log_with_path.append(f"{ctf_folder}/{i}")
	# """loop to populate lists with only ctffind4_PS.ctf files (list_2)"""
	# for i in file_list_all:
	# 	if 'PS.ctf' in i:
	# 		file_list_ctffind_4_PS.append(i)
	# """loop to populate list path+ctffind4_PS.ctf (list_3)"""
	# for i in file_list_ctffind_4_PS:
	# 	file_list_ctffind_4_PS_with_path.append(f"{ctf_folder}/{i}")

	if log_files:
		for fn in log_files:
			values = parse_ctffind(os.path.join(ctf_folder, fn))
			ctf_values.append((fn,) + values)
			parsed_files.append(fn)

		print(ctf_values[0])

		with open(os.path.join(ctf_folder, 'ctf_values.npy'), 'wb') as f:
			np.save(f, np.array(ctf_values,
								dtype=[('ctffile', 'U512'),
									   ('defocus1', 'f4'),
								       ('defocus2', 'f4'),
									   ('resolution', 'f4'),
									   ('azymuth', 'f4')
									   ]))

	time.sleep(10)

	# def avg_defocus(listdefocus1, listdefocus2):
	# 	avg_defocus_list = []
	# 	for i in range(0, len(listdefocus1)):
	# 		i_avg = (listdefocus1[i]+listdefocus2[i])/2
	# 		avg_defocus_list.append(i_avg)
	# 	return avg_defocus_list
    #
	# def delta_defoc(listdefocus1, listdefocus2):
	# 	delta_defocus_1 = []
	# 	for  i, i2 in zip(listdefocus1, listdefocus2):
	# 		dif = round(abs((i -i2)), 2)
	# 		delta_defocus_1.append(dif)
	# 	return 	delta_defocus_1
    #
	# ###
	# list_defocus_1 = extract_defocus_1(file_list_ctffind_4_log_with_path)
	# list_defocus_2 = extract_defocus_2(file_list_ctffind_4_log_with_path)
	# avg_defocus_glob = avg_defocus(list_defocus_1, list_defocus_2)
	# avg_defocus_glob_2f = []
	# resolution_list = extract_resolution(file_list_ctffind_4_log_with_path)
	# list_azymuth = extract_azymuth(file_list_ctffind_4_log_with_path)
	# list_defocus_dif = delta_defoc(list_defocus_1, list_defocus_2)
	# #reduce significant numbers to two###
	# for i in avg_defocus_glob:
	# 	i2 = float(f"{i:.2f}")
	# 	avg_defocus_glob_2f.append(i2)
	# ###write up pkl files with list for defocus_plotter###
	# with open('avg_defocus.pkl', 'wb') as f:
	# 	pickle.dump(avg_defocus_glob_2f, f)
	# with open('PS_ctf_files.pkl', 'wb') as f:
	# 	pickle.dump(file_list_ctffind_4_PS_with_path, f)
	# with open('resolution_list.pkl', 'wb') as f:
	# 	pickle.dump(resolution_list, f)
	# with open('azymuth.pkl', 'wb') as f:
	# 	pickle.dump(list_azymuth, f)
	# with open('defocus_dif.pkl', 'wb') as f:
	# 	pickle.dump(list_defocus_dif, f)
	# print(f"{list_defocus_dif[-10:]}")
    #
	# time.sleep(10)
