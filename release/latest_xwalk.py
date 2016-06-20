#!/usr/bin/env python3

'''
Get the latest version of Crosswalk binary from
https://linux-ftp.sh.intel.com/pub/mirrors/01org/crosswalk/releases/crosswalk/

Crosswalk for Android:
canary/beta/stable

Crosswalk for Windows:
canary/beta

Crosswalk for Deepin Linux
canary
'''

import os
import sys
import json
import argparse
import distutils.version
import urllib.parse

import requests
from bs4 import BeautifulSoup


PWD = os.getcwd()
SCRIPT_DIR = os.path.join(os.path.dirname(PWD), 'scripts')
sys.path.append(SCRIPT_DIR)

import xwalk


def read_json_config(config_file):
    configuration = None
    with open(config_file) as fp:
        configuration = json.load(fp)

    return configuration


def get_http_prefix(configuration, platform, branch_name):
    ver_url = None
    xwalk_http_prefix = configuration.get('http_aar_url_prefix')

    if platform == 'linux':
        ver_url = urllib.parse.urljoin(xwalk_http_prefix,
                                    '/'.join(['crosswalk',
                                        platform, 'deb', branch_name
                                    ]))
    else:
        ver_url = urllib.parse.urljoin(xwalk_http_prefix,
                                    '/'.join(['crosswalk',
                                        platform, branch_name
                                    ]))
    return ver_url.replace('https', 'http')


def detect_url_version(ver_url, filter_func):
    conn = requests.get(ver_url, verify = False)
    if not conn or not conn.content:
        sys.stderr.write('Failed to request {url}'.format(url = ver_url))
        sys.exit(1)

    soup = None
    soup = BeautifulSoup(conn.content, 'html.parser')
    ver_links = soup.find_all('a')
    versions = [v.string.strip('/') for v in filter(filter_func, ver_links)]
    if not versions:
        sys.stderr.write('{branch_name} branch version list is empty!'.format(
                        branch_name = branch_name))
        sys.exit(1)

    versions.sort(key = distutils.version.LooseVersion)
    latest_version = versions[-1]
    try:
        branch_num = int(latest_version.split('.')[0])
    except Exception:
        sys.stderr.write('latest version is invalid!')
        sys.exit(1)

    return (branch_num, latest_version)


def get_latest_version(ver_url, branch_name, filter_func):
    '''Get the latest verson of Crosswalk in a URL'''
    version_info = {}

    if branch_name == 'canary':
        branch = 'master'
    else:
        branch = branch_name

    version_info[branch] = {}

    (branch_num, latest_version) = detect_url_version(ver_url, filter_func)
    version_info[branch]['branch_name'] = branch_name
    if branch_name != 'beta':
        version_info[branch]['branch_number'] = branch_num
        version_info[branch]['latest_version'] = latest_version
    else:
        version_info[branch]['branch_number'] = []
        version_info[branch]['latest_version'] = []
        version_info[branch]['branch_number'].append(branch_num)
        version_info[branch]['latest_version'].append(latest_version)

    return version_info


def get_latest_beta_versions(ver_url, stable_branch_num, master_branch_num):
    beta_version_info = {}
    beta_version_info['beta'] = {}
    beta_version_info['beta']['branch_name'] = 'beta'
    beta_version_info['beta']['branch_number'] = []
    beta_version_info['beta']['latest_version'] = []

    for beta_branch_num in range(stable_branch_num + 1, master_branch_num):
        ver = get_latest_version(ver_url, 'beta', lambda link: \
                                                link.string != '../' and \
                                                link.string != 'latest/' and \
                                                link.string.startswith(str(
                                                    beta_branch_num
                                                )))
        beta_version_info['beta']['branch_number'].append(
                        ver['beta']['branch_number'])
        beta_version_info['beta']['latest_version'].append(
                        ver['beta']['latest_version'])

    return beta_version_info


def check_if_xwalk_ver_changed(origin_config,
                                master_ver, beta_ver, stable_ver, platform):
    if master_ver['master']['branch_number'] >= \
        origin_config['master']['branch_number'] and \
        distutils.version.LooseVersion(
            master_ver['master']['latest_version']) > \
        distutils.version.LooseVersion(
            origin_config['master']['latest_version']):
        return True

    if platform == 'android':
        if stable_ver['stable']['branch_number'] >= \
            origin_config['stable']['branch_number'] and \
            distutils.version.LooseVersion(
                stable_ver['stable']['latest_version']) > \
            distutils.version.LooseVersion(
                stable_ver['stable']['latest_version']):
            return True

    if platform == 'android' or platform == 'windows':
        if len(beta_ver['beta']['branch_number']) != \
            len(origin_config['beta']['branch_number']) and \
            len(beta_ver['beta']['latest_version']) != \
            len(origin_config['beta']['latest_version']):
            return True

        for i, latest_version in enumerate(beta_ver['beta']['latest_version']):
            if distutils.version.LooseVersion(latest_version) > \
                distutils.version.LooseVersion(
                    origin_config['beta']['latest_version'][i]):
                return True

    return False


def get_latest_android_xwalk(configuration, commandline_only = False):
    '''Get latest verson of Crosswalk for Android'''
    xwalk_android_ver_config = read_json_config(
                                'latest_android_xwalk_version.json')
    master_info = xwalk_android_ver_config.get('master')
    beta_info = xwalk_android_ver_config.get('beta')
    stable_info = xwalk_android_ver_config.get('stable')

    master_ver_url = get_http_prefix(configuration, 'android',
                        master_info.get('branch_name'))
    beta_ver_url = get_http_prefix(configuration, 'android',
                        beta_info.get('branch_name'))
    stable_ver_url = get_http_prefix(configuration, 'android',
                        stable_info.get('branch_name'))
    latest_master_ver_info = get_latest_version(master_ver_url, 'canary',
                                        lambda link: link.string != '../' and \
                                                    link.string != 'latest/')
    latest_stable_ver_info = get_latest_version(stable_ver_url, 'stable',
                                        lambda link: link.string != '../' and \
                                                    link.string != 'latest/')

    latest_beta_ver_info = get_latest_beta_versions(beta_ver_url,
                            latest_stable_ver_info['stable']['branch_number'],
                            latest_master_ver_info['master']['branch_number'])

    xwalk_android_ver_change = check_if_xwalk_ver_changed(
                                    xwalk_android_ver_config,
                                    latest_master_ver_info,
                                    latest_beta_ver_info,
                                    latest_stable_ver_info,
                                    platform = "android"
                                    )
    print(json.dumps(xwalk_android_ver_config, indent = 4, sort_keys = True))
    print('-' * 80)
    new_config = {}
    new_config.update(latest_master_ver_info)
    new_config.update(latest_beta_ver_info)
    new_config.update(latest_stable_ver_info)
    print(json.dumps(new_config, indent = 4, sort_keys = True))
    if xwalk_android_ver_change:
        if commandline_only:
            print('Write new latest versions to Android version config file.')
        else:
            with open('latest_android_xwalk_version.json', 'w') as f:
                json.dump(new_config, f, indent = 4, sort_keys = True)
    else:
        print('No Crosswalk for Android binary update!')


def get_latest_windows_xwalk(configuration, commandline_only = False):
    '''Get latest verson of Crosswalk for Windows'''
    xwalk_windows_ver_config = read_json_config(
                                'latest_windows_xwalk_version.json')
    master_info = xwalk_windows_ver_config.get('master')
    beta_info = xwalk_windows_ver_config.get('beta')

    master_ver_url = get_http_prefix(configuration, 'windows',
                        master_info.get('branch_name'))
    beta_ver_url = get_http_prefix(configuration, 'windows',
                        beta_info.get('branch_name'))

    latest_master_ver_info = get_latest_version(master_ver_url, 'canary',
                                        lambda link: link.string != '../' and \
                                                    link.string != 'latest/')
    latest_beta_ver_info = get_latest_version(beta_ver_url, 'beta',
                            lambda link: link.string != '../' and \
                                        link.string != 'latest/')
    xwalk_windows_ver_change = check_if_xwalk_ver_changed(
                                    xwalk_windows_ver_config,
                                    latest_master_ver_info,
                                    latest_beta_ver_info,
                                    None,
                                    platform = "windows"
                                    )
    print(json.dumps(xwalk_windows_ver_config, indent = 4, sort_keys = True))
    print('-' * 80)
    new_config = {}
    new_config.update(latest_master_ver_info)
    new_config.update(latest_beta_ver_info)
    print(json.dumps(new_config, indent = 4, sort_keys = True))
    if xwalk_windows_ver_change:
        if commandline_only:
            print('Write new latest versions to Windows version config file.')
        else:
            with open('latest_windows_xwalk_version.json', 'w') as f:
                json.dump(new_config, f, indent = 4, sort_keys = True)
    else:
        print('No Crosswalk for Windows binary update!')


def get_latest_linux_xwalk(configuration, commandline_only = False):
    '''Get the latest version of Crosswalk for Linux.'''
    xwalk_linux_ver_config = read_json_config(
                                'latest_linux_xwalk_version.json')
    master_info = xwalk_linux_ver_config.get('master')
    master_ver_url = get_http_prefix(configuration, 'linux',
                        master_info.get('branch_name'))

    latest_master_ver_info = get_latest_version(master_ver_url, 'canary',
                                        lambda link: link.string != '../' and \
                                                    link.string != 'latest/')
    xwalk_linux_ver_change = check_if_xwalk_ver_changed(
                                    xwalk_linux_ver_config,
                                    latest_master_ver_info,
                                    None,
                                    None,
                                    platform = "linux"
                                    )
    print(json.dumps(xwalk_linux_ver_config, indent = 4, sort_keys = True))
    print('-' * 80)
    new_config = {}
    new_config.update(latest_master_ver_info)
    print(json.dumps(new_config, indent = 4, sort_keys = True))
    if xwalk_linux_ver_change:
        if commandline_only:
            print('Write new latest versions to Linux version config file.')
        else:
            with open('latest_linux_xwalk_version.json', 'w') as f:
                json.dump(new_config, f, indent = 4, sort_keys = True)
    else:
        print('No Crosswalk for Linux binary update!')


def main():
    parser = argparse.ArgumentParser(description = \
                                    'Get the latest version of '\
                                    'Crosswalk binary.')
    parser.add_argument('-a', '--android', action = 'store_true',
                        default = True,
                        help = 'specify if only get the latest version of '\
                                'Crosswalk for Android')
    parser.add_argument('-w', '--windows', action = 'store_true',
                        help = 'specify if only get the latest version of '\
                                'Crosswalk for Windows')
    parser.add_argument('-x', '--linux', action = 'store_true',
                        help = 'specify if only get the latest version of '\
                                'Crosswalk for Deepin Linux')
    parser.add_argument('-c', '--commandline_only', action = 'store_true',
                        default = False,
                        help = 'only print the command line for development')
    args = parser.parse_args()
    if args.windows or args.linux:
        args.android = False

    config_file = os.path.join(SCRIPT_DIR, 'config.json')
    configuration = read_json_config(config_file)

    if args.android:
        get_latest_android_xwalk(configuration, args.commandline_only)

    if args.windows:
        get_latest_windows_xwalk(configuration, args.commandline_only)

    if args.linux:
        get_latest_linux_xwalk(configuration, args.commandline_only)


if __name__ == '__main__':
    main()
