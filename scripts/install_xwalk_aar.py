#!/usr/bin/env python3

import os
import json
import sys
import argparse


args = None

def download_aar(http_prefix, branch, xwalk_version, filename, aar_dir):
	os.chdir(aar_dir)
	url = 'wget --no-proxy --no-check-certificate {http_prefix}/{branch}/{xwalk_version}/{filename}'.format(
				http_prefix = http_prefix,
				branch = branch,
				xwalk_version = xwalk_version,
				filename = filename
		)
	if args.commandline:
		print(url)
	elif os.path.exists(os.path.join(aar_dir, filename)):
		print('{path} already exists!'.format(path = os.path.join(aar_dir, filename)))
	else:
		os.system(url)


def install_xwalk_aar(filename):
	data = None
	
	with open('config.json') as fp:
		data = json.load(fp)

	if data:
		http_prefix = data.get('http_aar_url_prefix')
		aar_dir = data.get('xwalk_aar_dir')
		aar_dir64 = data.get('xwalk_aar_dir64')

		(xwalk_version, ext) = os.path.splitext(filename)
		branch = None
		shared = False
		bit64 = False

		xwalk_version = xwalk_version.replace('crosswalk-', '')

		if 'shared' in filename:
			shared = True
			xwalk_version = xwalk_version.replace('shared-', '')

		if '64bit' in filename:
			bit64 = True
			xwalk_version = xwalk_version.replace('-64bit', '')

		if xwalk_version and xwalk_version.endswith('0'):
			branch = 'canary'
		else:
			branch = 'beta'

		if bit64:
			download_aar(http_prefix, branch, xwalk_version, filename, aar_dir64)
		else:
			download_aar(http_prefix, branch, xwalk_version, filename, aar_dir)

		cmd = 'mvn install:install-file -DgroupId=org.xwalk'
		if not shared:
			cmd += ' -DartifactId=xwalk_core_library' 
		else:
			cmd += ' -DartifactId=xwalk_shared_library'

		cmd += ' -Dversion={xwalk_version} -Dpackaging=aar'.format(xwalk_version = xwalk_version)
		cmd += ' -Dfile='
		if bit64:
			cmd += os.path.join(aar_dir64, filename)
		else:
			cmd += os.path.join(aar_dir, filename)

		cmd += ' -DgeneratePom=true'

		if bit64:
			cmd += ' -Dclassifier=64bit'

		if args.commandline:
			print(cmd)
		else:
			os.system(cmd)
	else:
		sys.exit(1)


def main():
	parser = argparse.ArgumentParser(description = 'Download an aar file and install it for cordova app building')
	parser.add_argument('-v', '--version', type = str, help = 'specify the crosswalk version')
	parser.add_argument('-l', '--long', action = 'store_true', help = 'specify if the crosswalk is 64bit')
	parser.add_argument('-s', '--shared', action = 'store_true', help = 'specifiy if the aar file for cordova app is shared')
	parser.add_argument('-c', '--commandline', action = 'store_true', help = 'only print the command line for development')

	global args 
	args = parser.parse_args()

	if len(sys.argv) < 2:
		parser.print_help()
		sys.exit(1)

	if bool(args.long) and bool(args.shared):
		sys.stderr.write('shared and 64bit should not coexist!\n')
		sys.exit(1)

	xwalk_version = None
	aar_filename_format = 'crosswalk{shared}-{version}{is64bit}.aar'
	if args.version:
		xwalk_version = args.version

	is64bit = ''
	if args.long:
		is64bit = '-64bit'

	shared = ''
	if args.shared:
		shared = '-shared'

	aar_filename = aar_filename_format.format(shared = shared, version = xwalk_version, is64bit = is64bit)

	install_xwalk_aar(aar_filename)


if __name__ == '__main__':
	main()