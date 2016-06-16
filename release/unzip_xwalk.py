#!/usr/bin/env python3

'''
Unzip all the zip files of a specific Crosswalk binary to default locations.
The default locations are set in the ../script/config.json
'''

import os
import sys
import json
import argparse

PWD = os.getcwd()
SCRIPT_DIR = os.path.join(os.path.dirname(PWD), 'scripts')
sys.path.append(SCRIPT_DIR)

import xwalk


def unzip_android_xwalk(configuration, xwalk_branch, xwalk_version,
                        commandline_only = False):
    # print('unzip android xwalk binary: {branch}->{version}'.format(
    #         branch = xwalk_branch, version = xwalk_version
    # ))
    android_config = None
    try:
        with open('android_xwalk.json') as f:
            android_config = json.loads(f.read())
    except Exception:
        sys.stderr.write('Failed to read android_xwalk.json, '\
                        'exit with 1\n')
        sys.exit(1)

    if not android_config:
        sys.stderr.write('Empty JSON data!')
        sys.exit(1)

    if xwalk_branch == 'master':
        xwalk_branch_name = 'canary'
    else:
        xwalk_branch_name = xwalk_branch

    android_all_dir_prefix = os.path.expanduser(configuration.get(
                                                'android_all_dir_prefix'))
    pkg_tools = os.path.expanduser(configuration.get('pkg_tools_dir'))
    pkg_tools64 = os.path.expanduser(configuration.get('pkg_tools_dir64'))
    branch_dir = os.path.join(android_all_dir_prefix, '{branch}'.format(
                                branch = xwalk_branch_name))
    version_dir = os.path.join(branch_dir, xwalk_version)

    arches = android_config.get('arches')
    arch_files = android_config.get('arch_files')
    non_arch_files = android_config.get('non_arch_files')

    for arch in arches:
        for file_template in arch_files:
            arch_dir = os.path.join(version_dir, arch)
            if arch.endswith('64'):
                dest_dir = pkg_tools64
            else:
                dest_dir = pkg_tools

            arch_file = file_template.format(version = xwalk_version,
                                            arch = arch)
            (arch_file_name, ext) = os.path.splitext(arch_file)
            unzip_arch_dir = os.path.join(dest_dir, arch_file_name)
            unzip_cmd = 'unzip {f} -d {d}'.format(f = arch_file, d = dest_dir)

            if commandline_only:
                print('cd {arch_dir}'.format(arch_dir = arch_dir))
            else:
                os.chdir(arch_dir)

            if not os.path.exists(unzip_arch_dir):
                if commandline_only:
                    print(unzip_cmd)
                else:
                    os.system(unzip_cmd)
            else:
                print('{d} already exists'.format(d = unzip_arch_dir))

    if commandline_only:
        print('cd {d}'.format(d = version_dir))
    else:
        os.chdir(version_dir)

    for non_arch_file_t in non_arch_files:
        non_arch_file = non_arch_file_t.format(version = xwalk_version)
        if '64bit' in non_arch_file:
            dest_dir = pkg_tools64
        else:
            dest_dir = pkg_tools

        (non_arch_filename, ext) = os.path.splitext(non_arch_file)
        unzip_non_arch_dir = os.path.join(dest_dir, non_arch_filename)
        if ext == '.zip':
            unzip_cmd = 'unzip {f} -d {d}'.format(f = non_arch_file,
                                                d = dest_dir)
            if not os.path.exists(unzip_non_arch_dir):
                if commandline_only:
                    print(unzip_cmd)
                else:
                    os.system(unzip_cmd)
        else:
            dest_file = os.path.join(dest_dir, non_arch_file)
            if not os.path.exists(dest_file):
                copy_cmd = 'cp -fv {src} {dest}'.format(
                                    src = non_arch_file,
                                    dest = dest_file)
                if commandline_only:
                    print(copy_cmd)
                else:
                    os.system(copy_cmd)
            else:
                print('{f} already exists!'.format(f = dest_file))


def unzip_windows_xwalk(configuration, xwalk_branch, xwalk_version,
                        commandline_only):
    windows_config = None
    try:
        with open('windows_xwalk.json') as f:
            windows_config = json.loads(f.read())
    except Exception:
        sys.stderr.write('Failed to read windows_xwalk.json, '\
                        'exit with 1\n')
        sys.exit(1)

    if not windows_config:
        sys.stderr.write('Empty JSON data!')
        sys.exit(1)

    if xwalk_branch == 'master':
        xwalk_branch_name = 'canary'
    else:
        xwalk_branch_name = xwalk_branch

    xwalk_win_dir = os.path.expanduser(configuration.get(
                                        'xwalk_win_dir'))
    xwalk_win_unzip_dir = os.path.expanduser(configuration.get(
                                        'xwalk_win_unzip_dir'))
    branch_dir = os.path.join(xwalk_win_dir, '{branch}'.format(
                                            branch = xwalk_branch_name))
    version_dir = os.path.join(branch_dir, xwalk_version)

    if xwalk_version > windows_config.get('xwalk_32bit_name_version'):
        is64bit = '64'
    else:
        is64bit = ''

    if commandline_only:
        print('cd {d}'.format(d = version_dir))
    else:
        os.chdir(version_dir)

    windows_xwalk_zip = windows_config.get('xwalk_zip_name').format(
                                        is64bit = is64bit,
                                        version = xwalk_version)
    (windows_xwalk_zip_filename, ext) = os.path.splitext(windows_xwalk_zip)
    dest_windows_xwalk_dir = os.path.join(xwalk_win_unzip_dir,
                                        windows_xwalk_zip_filename)

    if not os.path.exists(dest_windows_xwalk_dir):
        unzip_cmd = 'unzip {f} -d {d}'.format(f = windows_xwalk_zip,
                                            d = dest_windows_xwalk_dir)
        if commandline_only:
            print(unzip_cmd)
        else:
            os.system(unzip_cmd)
    else:
        print('{d} already exists!'.format(d = dest_windows_xwalk_dir))


def main():
    parser = argparse.ArgumentParser(description = 'Unzip all the zip files '\
                                    'of a specific Crosswalk binary to ' \
                                    'default locations')
    parser.add_argument('-v', '--version', type = str, required = True,
                        help = 'sepcify the Crosswalk binary version')
    parser.add_argument('-a', '--android', action = 'store_true',
                        default = True,
                        help = 'specify if unzip the Crosswalk binary for '\
                                'Android')
    parser.add_argument('-w', '--windows', action = 'store_true',
                        help = 'specify if unzip the Crosswalk binary for '\
                                'Windows')
    parser.add_argument('-c', '--commandline_only', action = 'store_true',
                        default = False,
                        help = 'only print the command line for development')
    args = parser.parse_args()
    if args.windows:
        args.android = False

    config_file = os.path.join(SCRIPT_DIR, 'config.json')
    configuration = None
    try:
        with open(config_file) as fp:
            configuration = json.load(fp)
    except Exception:
        sys.stderr.write('Failed to read json configuration ' \
                        'from ../script/config.json, exit with 1\n')
        sys.exit(1)

    xwalk_branch = xwalk.get_xwalk_branch(args.version)
    if args.android:
        unzip_android_xwalk(configuration, xwalk_branch, args.version,
                            args.commandline_only)
    if args.windows:
        unzip_windows_xwalk(configuration, xwalk_branch, args.version,
                            args.commandline_only)


if __name__ == '__main__':
    main()
