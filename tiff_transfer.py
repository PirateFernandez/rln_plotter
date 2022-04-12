import time
import os
import sys
try:
	origin_filepath = sys.argv[1]
except IndexError:
	print("### Wrong usage, please provide path to EPU folder in GSCEM###")
	print("Correct usage:")
	print("############################################################")
	print("pythonn3.x ln_files_from_gscem.py path_to_EPU_folder path_to_destination_folder")
	print("############################################################")
	print("### Please provide path to origin folder###")
	exit()
try:
	destiny_filepath = sys.argv[2]
except IndexError:
	print("### Wrong usage, please provide path to destination folder###")
	print("Correct usage:")
	print("############################################################")
	print("pythonn3.x ln_files_from_gscem.py path_to_origin_folder path_to_destination_folder")
	print("############################################################")
	print("### Please provide path to destination folder###")
	exit()
print(f"Origin folder: {origin_filepath}")
print(f"Destination folder: {destiny_filepath}")
gridsquares_folder = f"{origin_filepath}/Images-Disc1"
for i in range(576):
	list_gridsquares = os.listdir(gridsquares_folder)
	for i2 in list_gridsquares:
		grid_name = f"{origin_filepath}/Images-Disc1/{i2}/Data"	
		if os.path.isdir(grid_name) and len(os.listdir(grid_name)) > 10:	
			#print(grid_name)
			cmd = f"ln -sf {grid_name}/*s.tiff {destiny_filepath}"
			os.system(cmd)
	time.sleep(300)

