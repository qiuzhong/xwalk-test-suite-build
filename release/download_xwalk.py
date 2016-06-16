#!/usr/bin/env python3

import os
import sys
import json
import argparse
import urllib.parse

PWD = os.getcwd()
SCRIPT_DIR = os.path.join(os.path.dirname(PWD), 'scripts')
sys.path.append(SCRIPT_DIR)

import xwalk


def check_to_download(configuration, platform = 'android'):
    '''
    Check if the root directory is ready for downloading.
    '''
    if platform == 'android':
        android_all_dir_prefix = os.path.expanduser(configuration.get(
                                                        'android_all_dir_prefix'))
        if not os.path.exists(android_all_dir_prefix):
            return False
        master_dir = os.path.join(android_all_dir_prefix, '{master}'.format(
                                                            master = 'canary'))
        if not os.path.exists(master_dir):
            return False

        beta_dir = os.path.join(android_all_dir_prefix, '{beta}'.format(
                                                            beta = 'beta'))
        if not os.path.exists(beta_dir):
            return False

        stable_dir = os.path.join(android_all_dir_prefix, '{stable}'.format(
                                                            stable = 'stable'))
        if not os.path.exists(stable_dir):
            return False
    elif platform == 'windows':
        xwalk_win_dir_prefix = os.path.expanduser(configuration.get(
                                                    'xwalk_win_dir'))
        if not os.path.exists(xwalk_win_dir_prefix):
            return False

        master_dir = os.path.join(xwalk_win_dir_prefix, '{master}'.format(
                                                        master = 'canary'))
        if not os.path.exists(master_dir):
            return False

        beta_dir = os.path.join(xwalk_win_dir_prefix, '{beta}'.format(
                                                        beta = 'beta'))
        if not os.path.exists(beta_dir):
            return False
    elif platform == 'linux':
        xwalk_linux_dir_prefix = os.path.expanduser(configuration.get(
                                                    'xwalk_linux_dir'))
        if not os.path.exists(xwalk_linux_dir_prefix):
            return False

        master_dir = os.path.join(xwalk_linux_dir_prefix, '{master}'.format(
                                                            master = 'canary'))
        if not os.path.exists(master_dir):
            return False

    return True


def download_file(where, file_url, commandline_only = False):
    '''Download a file from
    https://linux-ftp.sh.intel.com/pub/mirrors/01org/ without https check.'''
    if commandline_only:
        print('cd {where}'.format(where = where))
    else:
        os.chdir(where)

    download_cmd = 'wget --no-proxy --no-check-certificate '
    download_cmd += file_url
    if commandline_only:
        print(download_cmd)
    else:
        os.system(download_cmd)


def download_android_xwalk(configuration, xwalk_branch, xwalk_version,
                            commandline_only = False):
    if not check_to_download(configuration, 'android'):
        sys.stderr.write('Not ready to download android xwalk binary!\n')
        return

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

    url_prefix = configuration.get('http_aar_url_prefix')
    android_all_dir_prefix = os.path.expanduser(configuration.get(
                                                'android_all_dir_prefix'))
    if xwalk_branch == 'master':
        xwalk_branch_name = 'canary'
    else:
        xwalk_branch_name = xwalk_branch

    branch_dir = os.path.join(android_all_dir_prefix, '{branch}'.format(
                                branch = xwalk_branch_name))
    if commandline_only:
        print('cd {d}'.format(d = branch_dir))
    else:
        os.chdir(branch_dir)

    # Create version directory
    version_dir = os.path.join(branch_dir, xwalk_version)
    if not os.path.exists(version_dir):
        mk_ver_dir_cmd = 'mkdir -pv {d}'.format(d = xwalk_version)
        if commandline_only:
            print(mk_ver_dir_cmd)
            print('cd {d}'.format(d = version_dir))
        else:
            os.system(mk_ver_dir_cmd)
            os.chdir(version_dir)

    arches = android_config.get('arches')
    arch_files = android_config.get('arch_files')
    non_arch_files = android_config.get('non_arch_files')

    for arch in arches:
        arch_dir = os.path.join(version_dir, arch)
        if not os.path.exists(arch_dir):
            mk_arch_dir_cmd = 'mkdir -pv {d}'.format(d = arch_dir)
            if commandline_only:
                print(mk_arch_dir_cmd)
            else:
                os.system(mk_arch_dir_cmd)


        for file_template in arch_files:
            arch_file_url = urllib.parse.urljoin(url_prefix, '/'.join(
                            ['crosswalk', 'android',
                            xwalk_branch_name, xwalk_version,
                            arch, file_template.format(
                                version = xwalk_version,
                                arch = arch
                            )]))
            local_arch_file = os.path.join(arch_dir, file_template.format(
                version = xwalk_version,
                arch = arch
            ))
            if not os.path.exists(local_arch_file):
                download_file(arch_dir, arch_file_url, commandline_only)
            else:
                print('{f} already exists!'.format(f = local_arch_file))

    if commandline_only:
        print('cd {d}'.format(d = version_dir))
    else:
        os.chdir(version_dir)

    for non_arch_file_t in non_arch_files:
        non_arch_file_url = urllib.parse.urljoin(url_prefix, '/'.join(
                            ['crosswalk', 'android',
                                xwalk_branch_name, xwalk_version,
                                non_arch_file_t.format(
                                    version = xwalk_version
                            )]))
        local_non_arch_file = os.path.join(version_dir,
                                non_arch_file_t.format(
                                    version = xwalk_version
                            ))
        if not os.path.exists(local_non_arch_file):
            download_file(version_dir, non_arch_file_url, commandline_only)
        else:
            print('{f} already exists!'.format(f = local_non_arch_file))


def download_windows_xwalk(configuration, xwalk_branch, xwalk_version,
                            commandline_only = False):
    if not check_to_download(configuration, 'windows'):
        sys.stderr.write('Not ready to download windows xwalk binary!\n')
        return

    windows_config = None
    try:
        with open('windows_xwalk.json') as f:
            windows_config = json.loads(f.read())
    except Exception:
        sys.stderr.write('Failed to read windows_xwalk.json, '\
                        'exit with 1\n')
        sys.exit(1)

    if xwalk_branch == 'master':
        xwalk_branch_name = 'canary'
    else:
        xwalk_branch_name = xwalk_branch

    url_prefix = configuration.get('http_aar_url_prefix')
    xwalk_win_dir_prefix = os.path.expanduser(configuration.get(
                                                'xwalk_win_dir'))
    branch_dir = os.path.join(xwalk_win_dir_prefix, '{branch}'.format(
                                branch = xwalk_branch_name))
    if commandline_only:
        print('cd {d}'.format(d = branch_dir))
    else:
        os.chdir(branch_dir)

    version_dir = os.path.join(branch_dir, xwalk_version)
    if not os.path.exists(version_dir):
        mk_ver_dir_cmd = 'mkdir -pv {d}'.format(d = xwalk_version)
        if commandline_only:
            print(mk_ver_dir_cmd)
            print('cd {d}'.format(d = version_dir))
        else:
            os.system(mk_ver_dir_cmd)
            os.chdir(version_dir)

    if xwalk_version > windows_config.get('xwalk_32bit_name_version'):
        is64bit = '64'
    else:
        is64bit = ''

    windows_xwalk_zip_template = windows_config.get('xwalk_zip_name')
    windows_xwalk_zip_url = urllib.parse.urljoin(url_prefix, '/'.join(
                            ['crosswalk', 'windows',
                            xwalk_branch_name, xwalk_version,
                            windows_xwalk_zip_template.format(
                                is64bit = is64bit,
                                version = xwalk_version
                            )]))
    local_windows_xwalk_zip = os.path.join(version_dir,
                            windows_xwalk_zip_template.format(
                                is64bit = is64bit,
                                version = xwalk_version
                            ))
    if not os.path.exists(local_windows_xwalk_zip):
        download_file(version_dir, windows_xwalk_zip_url, commandline_only)
    else:
        print('{f} already exists!'.format(f = local_windows_xwalk_zip))


def download_linux_xwalk(configuration, xwalk_branch, xwalk_version,
                        commandline_only = False):
    if not check_to_download(configuration, 'linux'):
        sys.stderr.write('Not ready to download linux xwalk binary!\n')
        return

    linux_config = None
    try:
        with open('linux_xwalk.json') as f:
            linux_config = json.loads(f.read())
    except Exception:
        sys.stderr.write('Failed to read linux_xwalk.json, '\
                        'exit with 1\n')
        sys.exit(1)

    if xwalk_branch == 'master':
        xwalk_branch_name = 'canary'
    else:
        xwalk_branch_name = xwalk_branch

    url_prefix = configuration.get('http_aar_url_prefix')
    xwalk_linux_dir_prefix = os.path.expanduser(configuration.get(
                                                'xwalk_linux_dir'))
    branch_dir = os.path.join(xwalk_linux_dir_prefix, '{branch}'.format(
                                                branch = xwalk_branch_name))
    if commandline_only:
        print('cd {d}'.format(d = branch_dir))
    else:
        os.chdir(branch_dir)

    version_dir = os.path.join(branch_dir, xwalk_version)
    if not os.path.exists(version_dir):
        mk_ver_dir_cmd = 'mkdir -pv {d}'.format(d = xwalk_version)
        if commandline_only:
            print(mk_ver_dir_cmd)
            print('cd {d}'.format(d = version_dir))
        else:
            os.system(mk_ver_dir_cmd)
            os.chdir(version_dir)

    arches = linux_config.get('arches')
    linux_deb_templates = linux_config.get('linux_xwalk_deb')
    for arch in arches:
        for linux_deb_template in linux_deb_templates:
            linux_xwalk_zip_url = urllib.parse.urljoin(url_prefix, '/'.join(
                                ['crosswalk', 'linux', 'deb',
                                xwalk_branch_name, xwalk_version,
                                linux_deb_template.format(
                                    version = xwalk_version,
                                    arch = arch
                                    )]))
            local_linux_xwalk_zip = os.path.join(version_dir,
                                    linux_deb_template.format(
                                        version = xwalk_version,
                                        arch = arch
                                    ))
            if not os.path.exists(local_linux_xwalk_zip):
                download_file(version_dir, linux_xwalk_zip_url,
                            commandline_only)
            else:
                print('{f} already exists!'.format(f = local_linux_xwalk_zip))


def main():
    parser = argparse.ArgumentParser(description = 'Download Crosswalk ' \
                                    'binary file with a specific version')
    parser.add_argument('-v', '--version', type = str, required = True,
                        help = 'specify the version of Crosswalk')
    parser.add_argument('-b', '--branch', type = str,
                        help = 'specify the branch of Crosswalk manually')
    parser.add_argument('-a', '--android', action = 'store_true',
                        default = True,
                        help = 'specify if the Crosswalk binary to download '\
                                'is for Android')
    parser.add_argument('-w', '--windows', action = 'store_true',
                        default = False,
                        help = 'specify if the Crosswalk binary to download '\
                                'is for Windows')
    parser.add_argument('-x', '--linux', action = 'store_true',
                        default = False,
                        help = 'specify if the Crosswalk binary to download '\
                                'is for Linux')
    parser.add_argument('-c', '--commandline_only', action = 'store_true',
                        default = False,
                        help = 'only print the command line for development')

    args = parser.parse_args()
    if args.windows and args.linux:
        sys.stderr.write('--windows and --linux options cannot coexist!\n')
        sys.exit(1)

    if args.windows or args.linux:
        args.android = False

    if not args.branch:
        xwalk_branch = xwalk.get_xwalk_branch(args.version)
    else:
        xwalk_branch = args.branch

    config_file = os.path.join(SCRIPT_DIR, 'config.json')
    configuration = None
    try:
        with open(config_file) as fp:
            configuration = json.load(fp)
    except Exception:
        sys.stderr.write('Failed to read json configuration ' \
                        'from ../script/config.json, exit with 1\n')
        sys.exit(1)

    if args.android:
        download_android_xwalk(configuration, xwalk_branch,
                                args.version, args.commandline_only)
    elif args.windows:
        download_windows_xwalk(configuration, xwalk_branch,
                                args.version, args.commandline_only)
    elif args.linux:
        download_linux_xwalk(configuration, xwalk_branch,
                                args.version, args.commandline_only)
    else:
        sys.stderr.write('Unknown platform, only android/windows/linux '\
                        'supported')
        sys.exit(1)


if __name__ == '__main__':
    main()
