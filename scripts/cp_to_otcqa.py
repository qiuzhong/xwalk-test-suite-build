#!/usr/bin/env python3

'''
This script try to copy the following type of packages to /mnt/otcqa
so that the test team in Dalian can get them from
http://otcqa.sh.intel.com
'''

import os
import sys
import json
import glob
import argparse

import xwalk


def mk_apk_cordova_dir(d_prefix, apk_d_prefix, cordova_d_prefix,
                        xwalk_branch, xwalk_version, mode, arch,
                        commandline_only = False):
    apk_d = os.path.join(d_prefix, xwalk_branch, xwalk_version,
                        '{apk_d_prefix}{mode}'.format(
                            apk_d_prefix = apk_d_prefix,
                            mode = mode),
                        arch)
    if not os.path.exists(apk_d):
        print('mkdir -pv {d}'.format(d = apk_d))
        os.makedirs(apk_d)

    cordova_d = os.path.join(d_prefix, xwalk_branch, xwalk_version,
                            '{cordova_d_prefix}{mode}'.format(
                                cordova_d_prefix = cordova_d_prefix,
                                mode = mode),
                            arch)
    if not os.path.exists(cordova_d):
        print('mkdir -pv {d}'.format(d = cordova_d))
        os.makedirs(cordova_d)


def check_configuration(configuration):
    '''Check if the configuration JSON data is valid'''
    jiajia_dir_prefix = configuration.get('android').get('jiajia_dir_prefix')
    if not jiajia_dir_prefix:
        sys.stderr.write('jiajia_dir_prefix is not set in cp_to_otcqa.json!')
        return False

    modes = configuration.get('android').get('modes')
    if not modes:
        sys.stderr.write('modes is not set in cp_to_otcqa.json!')
        return False

    arch32 = configuration.get('android').get('arch32')
    if not arch32:
        sys.stderr.write('arch32 is not set in cp_to_otcqa.json!')
        return False

    arch64 = configuration.get('android').get('arch64')
    if not arch64:
        sys.stderr.write('arch64 is not set in cp_to_otcqa.json!')
        return False

    jiajia_apk_prefix = configuration.get('android').get('jiajia_apk_prefix')
    if not jiajia_apk_prefix:
        sys.stderr.write('jiajia_apk_prefix is not set in cp_to_otcqa.json!')
        return False

    jiajia_cordova_prefix = configuration.get('android').get(
                                                    'jiajia_cordova_prefix')
    if not jiajia_cordova_prefix:
        sys.stderr.write('jiajia_cordova_prefix is not set '\
                        'in cp_to_otcqa.json!')
        return False

    otcqa_dir_prefix = configuration.get('android').get('otcqa_dir_prefix')
    if not otcqa_dir_prefix:
        sys.stderr.write('otcqa_dir_prefix is not set in cp_to_otcqa.json!')
        return False

    otcqa_apk_prefix = configuration.get('android').get('otcqa_apk_prefix')
    if not otcqa_apk_prefix:
        sys.stderr.write('otcqa_apk_prefix is not set in cp_to_otcqa.json!')
        return False

    otcqa_cordova_prefix = configuration.get('android').get(
                                                    'otcqa_cordova_prefix')
    if not otcqa_cordova_prefix:
        sys.stderr.write('otcqa_cordova_prefix is not set '\
                        'in cp_to_otcqa.json!')
        return False

    return True


def mkdir_jiajia(configuration, xwalk_branch, xwalk_version,
                commandline_only = False, is64bit = False):
    '''
    Create the necessory directory to
    /data/TestSuites_Storage/live/android/<branch>/<version>
    '''
    if not check_configuration(configuration):
        return False

    jiajia_dir_prefix = configuration.get('android').get('jiajia_dir_prefix')
    modes = configuration.get('android').get('modes')
    arch32 = configuration.get('android').get('arch32')
    arch64 = configuration.get('android').get('arch64')
    jiajia_apk_prefix = configuration.get('android').get('jiajia_apk_prefix')
    jiajia_cordova_prefix = configuration.get('android').get(
                                                    'jiajia_cordova_prefix')
    for mode in modes:
        for arch in arch32:
            try:
                mk_apk_cordova_dir(jiajia_dir_prefix,
                                jiajia_apk_prefix,
                                jiajia_cordova_prefix,
                                xwalk_branch, xwalk_version,
                                mode, arch)
            except Exception as e:
                sys.stderr.write('Failed to mkdir for arch32\n')
                print(e)
                return False

    if is64bit:
        for mode in modes:
            for arch in arch64:
                try:
                    mk_apk_cordova_dir(jiajia_dir_prefix,
                                    jiajia_apk_prefix,
                                    jiajia_cordova_prefix,
                                    xwalk_branch, xwalk_version,
                                    mode, arch)
                except Exception:
                    sys.stderr.write('Failed to mkdir for arch64')
                    return False
    return True


def mkdir_otcqa(configuration, xwalk_branch, xwalk_version, is64bit = False):
    '''
    Create the necessory directory to
    /mnt/otcqa/2016/live/crosswalk/android/<branch>/<version>
    '''
    if not check_configuration(configuration):
        return False

    jiajia_dir_prefix = configuration.get('android').get('jiajia_dir_prefix')
    jiajia_apk_prefix = configuration.get('android').get('jiajia_apk_prefix')
    jiajia_cordova_prefix = configuration.get('android').get(
                                                    'jiajia_cordova_prefix')
    otcqa_dir_prefix = configuration.get('android').get('otcqa_dir_prefix')
    otcqa_apk_prefix = configuration.get('android').get('otcqa_apk_prefix')
    otcqa_cordova_prefix = configuration.get('android').get(
                                                    'otcqa_cordova_prefix')
    modes = configuration.get('android').get('modes')
    arch32 = configuration.get('android').get('arch32')
    arch64 = configuration.get('android').get('arch64')

    for mode in modes:
        for arch in arch32:
            try:
                mk_apk_cordova_dir(otcqa_dir_prefix,
                                otcqa_apk_prefix,
                                otcqa_cordova_prefix,
                                xwalk_branch, xwalk_version,
                                mode, arch)
            except Exception as e:
                sys.stderr.write('Failed to mkdir for arch32\n')
                print(e)
                return False

    if is64bit:
        for mode in modes:
            for arch in arch64:
                try:
                    mk_apk_cordova_dir(otcqa_dir_prefix,
                                    otcqa_apk_prefix,
                                    otcqa_cordova_prefix,
                                    xwalk_branch, xwalk_version,
                                    mode, arch)
                except Exception:
                    sys.stderr.write('Failed to mkdir for arch64')
                    return False
    return True


def cp_to_otcqa(configuration, xwalk_branch, xwalk_version,
                package_type = 'all',
                commandline_only = False,
                force = False,
                is64bit = False):
    '''Copy package from jiajia directory to otcqa.'''
    if not check_configuration(configuration):
        return False

    jiajia_dir_prefix = configuration.get('android').get('jiajia_dir_prefix')
    jiajia_apk_prefix = configuration.get('android').get('jiajia_apk_prefix')
    jiajia_cordova_prefix = configuration.get('android').get(
                                                    'jiajia_cordova_prefix')
    otcqa_dir_prefix = configuration.get('android').get('otcqa_dir_prefix')
    otcqa_apk_prefix = configuration.get('android').get('otcqa_apk_prefix')
    otcqa_cordova_prefix = configuration.get('android').get(
                                                    'otcqa_cordova_prefix')
    modes = configuration.get('android').get('modes')
    arch32 = configuration.get('android').get('arch32')
    arch64 = configuration.get('android').get('arch64')

    if package_type != 'all' and package_type != "aio":
        for mode in modes:
            for arch in arch32:
                src_apk_d = os.path.join(jiajia_dir_prefix,
                                        xwalk_branch,
                                        xwalk_version,
                                        '{apk_d_prefix}{mode}'.format(
                                            apk_d_prefix = jiajia_apk_prefix,
                                            mode = mode),
                                        arch)
                if commandline_only:
                    print('cd {d}'.format(d = src_apk_d))
                os.chdir(src_apk_d)
                zip_files = glob.glob('*.zip')
                if not zip_files:
                    continue

                packages = [package for package in zip_files if
                            package_type in package]
                if not packages:
                    continue

                dest_apk_d = os.path.join(otcqa_dir_prefix,
                                        xwalk_branch,
                                        xwalk_version,
                                        '{apk_d_prefix}{mode}'.format(
                                            apk_d_prefix = otcqa_apk_prefix,
                                            mode = mode),
                                        arch)
                for package in packages:
                    src_zip = os.path.join(src_apk_d, package)
                    dest_zip = os.path.join(dest_apk_d, package)

                    cp_cmd = 'cp -fv {src} {dest}'.format(src = src_zip,
                                                    dest = dest_zip)
                    if commandline_only:
                        print(cp_cmd)
                    else:
                        if not os.path.exists(dest_zip) or force:
                            os.system(cp_cmd)


    return True


def main():
    parser = argparse.ArgumentParser(description = 'Copy test suite packages '\
                                                    'from jiajia directory ' \
                                                    'to otcqa server.')
    parser.add_argument('-v', '--version', type = str, required = True,
                        help = 'specify the Crosswalk version')
    parser.add_argument('-p', '--package_type', type = str, required = True,
                        help = 'specify which kind of packages to be copied ' \
                                'from jiajia directory to otcqa server')
    parser.add_argument('-l', '--long', action = 'store_true',
                        help = 'specify if also copy the 64bit packages')
    parser.add_argument('-c', '--commandline_only', action = 'store_true',
                        help = 'specify if print command line only')
    parser.add_argument('-f', '--force', action = 'store_true',
                        help = 'specify if copy the package to otcqa by force')
    args = parser.parse_args()

    xwalk_branch = xwalk.get_xwalk_branch(args.version)
    conf_filename = __file__.replace('.py', '.json')
    configuration = None
    with open(conf_filename) as f:
        configuration = json.load(f)

    if not configuration:
        sys.stderr.write('Invalid JSON content in cp_to_otcqa.json or empty!')
        sys.exit(1)

    if mkdir_jiajia(configuration, xwalk_branch, args.version,
                    args.commandline_only, args.long):
        cp_to_otcqa(configuration, xwalk_branch, args.version,
                    args.package_type,
                    args.commandline_only,
                    args.force,
                    args.long)


if __name__ == '__main__':
    main()
