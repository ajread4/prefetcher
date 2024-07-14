import argparse
import pyscca 


# Analyze the provided Prefetch File 
def analyze_file(file):
	file_pyscca = pyscca.open(file)

	print(f"Analyzing: {str(file)}" )
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

	print("\n\nVolume Information\n")

	for volume in range(0,total_num_volumes):
		volume_pyscca=file_pyscca.get_volume_information(volume)
		print(volume_pyscca.get_device_path())

def main():
	"""
	Main function for prefetcher
	"""
	parser = argparse.ArgumentParser(description='Prefetcher - Parse Windows 10 Prefetch Files')
	parser.add_argument('prefetch_file', action='store', help='prefetch file to analyze',metavar='prefetch_file')

	args = parser.parse_args()

	analyze_file(args.prefetch_file)

if __name__=="__main__":
	try:
		main()
	except Exception as err:
		print(repr(err))