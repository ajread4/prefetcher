#!/usr/bin/env python3
#   Written by AJ Read (ajread4) with help/inspiration from w10pf_parser.py written by David Cruciani. 
#
#   Purpose: Parse prefetch files for executable name, run count, run times, referenced files, and number of volumes. 
#   Details: The prefetch file or directory is passed to the main function using the command line. If only a single file, the prefetch file is parse using pyscca. If the input is a directory, a directory function calls the file function as it loops through each file in the directory.
#

import argparse
import pyscca 
import glob
import json


# Analyze the provided Prefetch File 
def analyze_file(file,output_json):

	try: 
		file_pyscca = pyscca.open(file)

		if not output_json:

			print(f"\nAnalyzing: {str(file)}" )
			print(f'\nExecutable Name: {str(file_pyscca.get_executable_filename())}')

		# Determine and Print the Run Count
		run_count=int(file_pyscca.get_run_count())

		if not output_json:
			print(f"\nRun Count: {str(run_count)}")

			# Since prefetch only has the last 8 run times 
		if run_count > 8:
			run_count=8

		# Print the Prefetch Run Times
		store_runtime={}
		for r in range(0,run_count):
			if not output_json:
				print(f"Run Time:  {str(file_pyscca.get_last_run_time(r))}")
			else: 
				store_runtime.update({"Run " + str(r+1) :str(file_pyscca.get_last_run_time(r))})


		# Determine the Number of Files
		total_num_files=int(file_pyscca.get_number_of_file_metrics_entries())
		total_num_volumes=int(file_pyscca.get_number_of_volumes())

		if not output_json:
			# Return the Number of Referenced Files
			print(f"\nTotal Number of Files: {str(total_num_files)}")
			print(f"Total Number of Volumes: {str(total_num_volumes)}")
			

			print("\nFiles Referenced\n")

		# Print the Number of File Names
		store_file_names={}
		for enum_file in range(0,total_num_files):
			if not output_json:
				print(file_pyscca.get_filename(enum_file))
			else:
				store_file_names.update({"File " + str(enum_file+1):file_pyscca.get_filename(enum_file)})

		if not output_json:
			print("\nVolume Information")

		store_volume_info={}
		for volume in range(0,total_num_volumes):
			volume_pyscca=file_pyscca.get_volume_information(volume)
			if not output_json:
				print(volume_pyscca.get_device_path())
			else: 
				store_volume_info.update({"Volume " + str(volume+1):str(volume_pyscca.get_device_path())})

		# If JSON output is requested by the user
		output_dict={}
		if output_json:
			output_dict.update({"filename":str(file),"executable_name":file_pyscca.get_executable_filename(),"run_times":store_runtime,"num_files":total_num_files,"files":store_file_names,"num_volumes":total_num_volumes,"volume_information":store_volume_info})
			print(json.dumps(output_dict))		

	# If pyscca is not able to parse the prefetch file
	except OSError:
		if not output_json:
			print(f"Unable to parse prefetch: {str(file)}")
		else:
			output_dict={}
			output_dict.update({"filename":str(file)})
			print(json.dumps(output_dict))

# Analyze the provided Prefetch File directory
def analyze_dir(input_dir,output_json):

	for filepath in glob.iglob(input_dir + '/*.pf'):
		if output_json:
			analyze_file(filepath,True)
		else: 
			print(f"Analyzing Directory: {str(input_dir)}" )
			analyze_file(filepath,False)
			print("--------------------------------------------------------------------------------")

def main():
	"""
	Main function for prefetcher
	"""
	parser = argparse.ArgumentParser(description='Prefetcher - Parse Windows 10 Prefetch Files')
	parser.add_argument('-f','--file', action='store', help='prefetch file to analyze',metavar='prefetch_file')
	parser.add_argument('-d','--directory',action='store',help='directory of prefetch files to analyze', metavar='prefetch_directory')
	parser.add_argument('-j','--json',action='store_true',help='output results to json')

	args = parser.parse_args()

	if args.file and args.json: 
		analyze_file(args.file,output_json=True)
	elif args.file:
		analyze_file(args.file,output_json=False)
	elif args.directory and args.json:
		analyze_dir(args.directory,output_json=True)
	elif args.directory:
		analyze_dir(args.directory,output_json=False)


if __name__=="__main__":
	try:
		main()
	except Exception as err:
		print(repr(err))