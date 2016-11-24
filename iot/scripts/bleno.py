#!/usr/bin/env python3

import sys
import argparse


lines = []

def parse_bleno_results_log(bleno_log_file):
	'''
	Process the log file to csv format.
	'''
	global lines
	with open(bleno_log_file) as fp:
		for line in fp:
			if not line.strip():
				continue
			old_test_case_id = line.strip().split('"')[-2]
			new_test_case_id = old_test_case_id.replace(' ', '_')
			new_line = line.replace('"' + old_test_case_id + '"', 
									new_test_case_id)
			lines.append(new_line)


def write_bleno_results_log(bleno_log_file):
	'''
	Write the new lines with test case id without any blank spaces to 
	result-bleno.log.bak Add a newline to the end of the file.
	'''
	global lines
	with open(bleno_log_file + '.bak', 'w') as fp:
		fp.writelines(lines)
		fp.write('\n')


def main():
    parser = argparse.ArgumentParser(description = \
    		'Convert the bleno test case id with blank spaces ' \
    		'to underscore-connected.')
    parser.add_argument('-f', '--file', type = str, required = True,
                        help = 'specify the absolute path of result-bleno.log')
    args = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    parse_bleno_results_log(log_file)
    write_bleno_results_log(log_file)



if __name__ == '__main__':
	main()