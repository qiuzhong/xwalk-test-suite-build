#!/usr/bin/env python3

import os
import sys
import json
import argparse

import xwalk


def unzip_cordova_zip(dir_prefix, xwalk_branch, xwalk_version, mode, arch,
                        cordova_prefix = 'cordova4.x', clean = True):
    zip_dir = os.path.join(dir_prefix, xwalk_branch, xwalk_version,
                            cordova_prefix + '-' + mode, arch)
    zip_file = '{cordova_prefix}_sampleapp_{arch}.zip'.format(
                            cordova_prefix = cordova_prefix, arch = arch)

    if not os.path.exists(zip_dir):
        sys.stderr.write('{zip_dir} does not exist!\n'.format(
                        zip_dir = zip_dir))
        return False

    elif not os.path.exists(os.path.join(zip_dir, zip_file)):
        sys.stderr.write('{zip_file} does not exist!\n'.format(
                        zip_file = zip_file))
        return False

    else:
        os.chdir(zip_dir)
        os.system('unzip {zip_file}'.format(zip_file = zip_file))
        if clean:
            os.remove(zip_file)

    return True


def main():

    parser = argparse.ArgumentParser(description =  \
                                    'Unzip the cordova4.x_sampleapp_arm.zip '\
                                    'to separate apk files.')
    parser.add_argument('-v', '--version', type = str, required = True,
                        help = 'specify the crosswalk version')
    parser.add_argument('-b', '--branch', type = str,
                        help = 'specify the branch of Crosswalk manually')
    parser.add_argument('-a', '--arch', type = str, required = True,
                        help = 'specify the CPU architecture, '\
                                'arm/arm64/x86/x86_64')
    parser.add_argument('-m', '--mode', type = str, required = True,
                        help = 'specify the crosswalk application mode, ' \
                                'embedded/shared')

    parser.add_argument('-c', '--complete', action = 'store_true',
                        default = False,
                        help =  'specify if unzip all the zip files of ' \
                                'all arch CPUs and all modes')
    parser.add_argument('-j', '--jiajia', action = 'store_true',
                        default = True,
                        help = 'specify if unzip the ' \
                                'cordova4.x_sampleapp_arm.zip in '\
                                'jiajia directory')
    parser.add_argument('-q', '--otcqa', action = 'store_true',
                        default = False,
                        help =  'specify if unzip the '\
                                'cordova4.x_sampleapp_arm.zip in otcqa server')

    args = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    if not args.version:
        sys.stderr.write('No Crosswalk version specified, exit with 1\n')
        sys.exit(1)
    if not xwalk.check_xwalk_version_valid(args.version):
        sys.stderr.write('Invalid Crosswalk version!\n')
        sys.exit(1)

    configuration = None
    try:
        with open('config.json') as fp:
            configuration = json.load(fp)
    except Exception:
        sys.stderr.write('Failed to read json configuration ' \
                        'from config.json, exit with 1\n')
        sys.exit(1)

    if not configuration:
        sys.write.write('Configuration is empty, exit with 1\n')
        sys.exit(1)

    xwalk_branch = None
    if not args.branch:
        xwalk_branch = xwalk.get_xwalk_branch(args.version)
    else:
        xwalk_branch = args.branch

    if args.complete and not args.arch and not args.mode and not args.otcqa:
        for mode in ('embedded', 'shared'):
            for arch in ('arm', 'arm64'):
                if unzip_cordova_zip(configuration.get('jiajia_dir_prefix'),
                                    xwalk_branch, args.version, mode, arch):
                    print('unzip {xwalk_version} cordova ' \
                        '{mode} {arch} successfully!'.format(
                                xwalk_version = args.version,
                                mode = mode,
                                arch = arch))
                else:
                    print('Failed to unzip {xwalk_version} cordova ' \
                        '{mode} {arch}!'.format(
                                xwalk_version = args.version,
                                mode = mode,
                                arch = arch))

    if not args.complete and not args.otcqa and args.arch and args.mode:
        if unzip_cordova_zip(configuration.get('jiajia_dir_prefix'),
                            xwalk_branch, args.version, args.mode, args.arch):
            print('unzip {xwalk_version} cordova ' \
                    '{mode} {arch} successfully!'.format(
                                xwalk_version = args.version,
                                mode = args.mode,
                                arch = args.arch))
        else:
            print('Failed to unzip {xwalk_version} cordova ' \
                    '{mode} {arch}!'.format(
                                xwalk_version = args.version,
                                mode = args.mode,
                                arch = args.arch))

    if args.otcqa and args.arch and args.mode:
        if unzip_cordova_zip(configuration.get('otcqa_dir_prefix'),
                            xwalk_branch, args.version, args.mode, args.arch):
            print('unzip {xwalk_version} cordova ' \
                    '{mode} {arch} successfully!'.format(
                            xwalk_version = args.version,
                            mode = args.mode,
                            arch = args.arch))
        else:
            print('unzip {xwalk_version} cordova ' \
                    '{mode} {arch} successfully!'.format(
                            xwalk_version = args.version,
                            mode = args.mode,
                            arch = args.arch))


if __name__ == '__main__':
    main()
