import time
import os
import sys
try:
	origin_filepath = sys.argv[1]
except IndexError:
	print("### Wrong usage, please provide path to origin folder.###")
	print("Correct usage:")
	print("############################################################")
	print("pythonn3.x ln_files_from_gscem.py path_to_origin_folder path_to_destination_folder")
	print("############################################################")
	print("### Please provide path to origin folder. ###")
	exit()
try:
	destiny_filepath = sys.argv[2]
except IndexError:
	print("### Wrong usage, please provide path to destination folder.###")
	print("Correct usage:")
	print("############################################################")
	print("pythonn3.x ln_files_from_gscem.py path_to_origin_folder path_to_destination_folder")
	print("############################################################")
	print("### Please provide path to destination folder. ###")
	exit()
print(f"Origin folder: {origin_filepath}")
print(f"Destination folder: {destiny_filepath}")
cmd = f"ln -sf {origin_filepath}/*.tiff {destiny_filepath}/"
#os.system(cmd)
for i in range(96):
	os.system(cmd)
	time.sleep(1800)
