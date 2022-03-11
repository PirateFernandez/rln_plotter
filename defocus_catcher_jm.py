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

	if log_files:
		for fn in log_files:
			values = parse_ctffind(os.path.join(ctf_folder, fn))
			ctf_values.append((fn,) + values)
			parsed_files.append(fn)

		with open(os.path.join(ctf_folder, 'ctf_values.npy'), 'wb') as f:
			np.save(f, np.array(ctf_values,
								dtype=[('ctffile', 'U512'),
									   ('defocus1', 'f4'),
								       ('defocus2', 'f4'),
									   ('resolution', 'f4'),
									   ('azymuth', 'f4')
									   ]))

	time.sleep(10)
