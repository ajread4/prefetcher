#!/usr/bin/env python3
#   Written by AJ Read (ajread4) with help/inspiration from w10pf_parser.py written by David Cruciani. 
#
#   Purpose: Parse prefetch files for executable name, run count, run times, referenced files, and number of volumes. 
#   Details: The prefetch file or directory is passed to the main function using the command line. If only a single file, the prefetch file is parse using pyscca. If the input is a directory, a directory function calls the file function as it loops through each file in the directory.
#

import argparse
import pyscca 
import glob


# Analyze the provided Prefetch File 
def analyze_file(file):

	try: 
		file_pyscca = pyscca.open(file)

		print(f"\nAnalyzing: {str(file)}" )
		print(f'\nExecutable Name: {str(file_pyscca.get_executable_filename())}')

		# Determine and Print the Run Count
		run_count=int(file_pyscca.get_run_count())
		print(f"\nRun Count: {str(run_count)}")

		# Since prefetch only has the last 8 run times 
		if run_count > 8:
			run_count=8

		# Print the Prefetch Run Times
		for r in range(0,run_count):
			print(f"Run Time:  {str(file_pyscca.get_last_run_time(r))}")


		# Determine the Number of Files
		total_num_files=int(file_pyscca.get_number_of_file_metrics_entries())
		total_num_volumes=int(file_pyscca.get_number_of_volumes())

		# Return the Number of Referenced Files
		print(f"\nTotal Number of Files: {str(total_num_files)}")
		print(f"Total Number of Volumes: {str(total_num_volumes)}")
		

		print("\nFiles Referenced\n")

		# Print the Number of File Names
		for file in range(0,total_num_files):
			print(file_pyscca.get_filename(file))

		print("\nVolume Information")

		for volume in range(0,total_num_volumes):
			volume_pyscca=file_pyscca.get_volume_information(volume)
			print(volume_pyscca.get_device_path())

	# If pyscca is not able to parse the prefetch file
	except OSError:
		print(f"Unable to parse prefetch: {str(file)}")

# Analyze the provided Prefetch File directory
def analyze_dir(input_dir):
	print(f"Analyzing Directory: {str(input_dir)}" )

	for filepath in glob.iglob(input_dir + '/*.pf'):
		analyze_file(filepath)
		print("--------------------------------------------------------------------------------")


def main():
	"""
	Main function for prefetcher
	"""
	parser = argparse.ArgumentParser(description='Prefetcher - Parse Windows 10 Prefetch Files')
	parser.add_argument('-f','--file', action='store', help='prefetch file to analyze',metavar='prefetch_file')
	parser.add_argument('-d','--directory',action='store',help='directory of prefetch files to analyze', metavar='prefetch_directory')

	args = parser.parse_args()

	if args.file: 
		analyze_file(args.file)
	else:
		analyze_dir(args.directory)

if __name__=="__main__":
	try:
		main()
	except Exception as err:
		print(repr(err))