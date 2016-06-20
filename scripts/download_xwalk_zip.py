#!/usr/bin/env python3

import os
import json
import sys
import argparse

import xwalk

args = None


def download_file(http_prefix, branch, xwalk_version, filename, zip_dir,
					platform = 'android'):

	xwalk_type = ''
	if platform == 'linux':
		xwalk_type = '/deb'

	if args.commandline:
		print('cd {zip_dir}'.format(zip_dir = zip_dir))
	os.chdir(zip_dir)

	url = 'wget --no-proxy --no-check-certificate ' \
			'{http_prefix}/{platform}{extra}/' \
			'{branch}/{xwalk_version}/{filename}'.format(
				http_prefix = http_prefix,
				platform = platform,
				extra = xwalk_type,
				branch = branch,
				xwalk_version = xwalk_version,
				filename = filename
		)
	if args.commandline:
		print(url)
	elif os.path.exists(os.path.join(zip_dir, filename)):
		print('{path} already exists!'.format(path = os.path.join(zip_dir,
																filename)))
	else:
		os.system(url)


def download_xwalk_zip(filename, platform = 'android'):
	data = None

	with open('config.json') as fp:
		data = json.load(fp)

	if data:
		http_prefix = data.get('http_aar_url_prefix')
		android_zip_dir = os.path.expanduser(data.get('xwalk_zip_dir'))
		windows_zip_dir = os.path.expanduser(data.get('xwalk_win_dir'))
		linux_deb_dir = os.path.expanduser(data.get('xwalk_linux_dir'))

		(xwalk_version, ext) = os.path.splitext(filename)
		branch = None
		shared = False
		bit64 = False

		xwalk_version = xwalk_version.replace('crosswalk-', '')
		xwalk_version = xwalk_version.replace('crosswalk64-', '')
		xwalk_version = xwalk_version.replace('crosswalk_', '')

		if '64bit' in filename:
			bit64 = True
			xwalk_version = xwalk_version.replace('-64bit', '')

		if xwalk_version.endswith('-1_amd64'):
			xwalk_version = xwalk_version.replace('-1_amd64', '')
		if xwalk_version.endswith('-1_i386'):
			xwalk_version = xwalk_version.replace('-1_i386', '')

		if xwalk_version and xwalk_version.endswith('.0'):
			branch = 'canary'
		else:
			branch = 'beta'

		if platform == 'android':
			download_file(http_prefix, branch, xwalk_version, filename,
						android_zip_dir)
		elif platform == 'windows':
			download_file(http_prefix, branch, xwalk_version, filename,
						windows_zip_dir, platform)
		elif platform == 'linux':
			download_file(http_prefix, branch, xwalk_version, filename,
						linux_deb_dir, platform)
		else:
			sys.stderr.write('Not supported platform!\n')
			sys.exit(1)
	else:
		sys.exit(1)


def main():
	parser = argparse.ArgumentParser(description = \
									'Download a crosswalk zip file.')
	parser.add_argument('-v', '--version', type = str, required = True,
						help = 'specify the crosswalk version')
	parser.add_argument('-l', '--long', action = 'store_true',
						help = 'specify if the crosswalk is 64bit')
	parser.add_argument('-a', '--android', action = 'store_true',
						default = True,
						help = 	'specify if the crosswalk is for Android, ' \
								'default option')
	parser.add_argument('-w', '--windows', action = 'store_true',
						help = 'specify if the crosswalk is for Windows')
	parser.add_argument('-x', '--linux', action = 'store_true',
						help = 'specify if the crosswalk is for Linux')
	parser.add_argument('-c', '--commandline', action = 'store_true',
						help = 'only print the command line for development')

	global args
	args = parser.parse_args()

	if len(sys.argv) < 2:
		parser.print_help()
		sys.exit(1)

	if args.long and args.windows:
		sys.stderr.write('Crosswalk for Windows has not 64bit edition!\n')
		sys.exit(1)

	if args.windows or args.linux:
		args.android = False

	zip_filename_format = 'crosswalk-{version}{is64bit}.zip'
	win_filename_format = 'crosswalk{has64}-{version}{is64bit}.zip'
	deb_filename_format = 'crosswalk_{version}-1_{arch}.deb'
	xwalk_version = None

	if not xwalk.check_xwalk_version_valid(args.version):
		sys.stderr.write('Invalid Crosswalk version!\n')
		sys.exit(1)

	if args.version:
		xwalk_version = args.version

	is64bit = ''
	arch = 'i386'
	if args.long:
		is64bit = '-64bit'
		arch = 'amd64'

	platform = None
	if args.android:
		platform = 'android'
	elif args.windows:
		platform = 'windows'
	elif args.linux:
		platform = 'linux'
	else:
		sys.stderr.write('Platform can only be android, windows and linux!\n')
		sys.exit(1)

	if xwalk_version:
		zip_filename = zip_filename_format.format(version = xwalk_version,
												is64bit = is64bit)
		deb_filename = deb_filename_format.format(version = xwalk_version,
												arch = arch)

		# After 19.48.495.0. the crosswalk
		has64 = ''
		if xwalk_version > '19.48.495.0':
			has64 = '64'
		win_filename = win_filename_format.format(has64 = has64,
												version = xwalk_version,
												is64bit = is64bit)

	if args.linux:
		download_xwalk_zip(deb_filename, platform)
	elif args.windows:
		download_xwalk_zip(win_filename, platform)
	else:
		download_xwalk_zip(zip_filename, platform)


if __name__ == '__main__':
	main()
