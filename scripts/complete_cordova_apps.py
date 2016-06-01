#!/usr/bin/env python3


import os
import sys
import glob
import json
import argparse

import xwalk

# PWD = None

def get_missing_cordova_apps(configuration,
                             xwalk_branch,
                             xwalk_version,
                             mode,
                             arch,
                             cordova_prefix = 'cordova4.x'):
    '''Check the missing cordova apps and return a list.'''
    missing_cordova_apps = None
    cordova_config = None
    try:
        with open('cordova_apps.json') as f:
            cordova_config = json.load(f)
    except Exception:
        sys.stderr.write('Failed to read json configuration from ' \
                         'cordova_apps.json, exit with 1\n')
        sys.exit(1)

    if not cordova_config:
        sys.write.write('Cordova configuration is empty, exit with 1\n')
        sys.exit(1)

    branch_num = xwalk_version.split('.')[0]
    all_cordova_apps = cordova_config.get(branch_num)
    if not all_cordova_apps:
        sys.stderr.write('Cordova app list is empty, exit with 1\n')
        sys.exit(1)

    cordova_apps_dir = os.path.join(configuration.get('jiajia_dir_prefix'),
                                    xwalk_branch,
                                    xwalk_version,
                                    cordova_prefix + '-' + mode,
                                    arch)
    if not os.path.exists(cordova_apps_dir):
        sys.stderr.write('{cordova_apps_dir} does not exist!\n'.format(
                        cordova_apps_dir = cordova_apps_dir))
        return all_cordova_apps

    os.chdir(cordova_apps_dir)
    present_cordova_apks = glob.glob('*.apk')
    present_cordova_apps = [apk.rstrip('.apk') for apk in present_cordova_apks]

    missing_cordova_apps = list(
                        set(all_cordova_apps) - set(present_cordova_apps))
    missing_cordova_apps.sort()

    return missing_cordova_apps


def build_missing_cordova_apps(missing_apps,
                            configuration,
                            xwalk_branch,
                            xwalk_version,
                            mode,
                            arch):
    '''Build the missing cordova apps and copy them to jiajia directory.'''
    global PWD
    os.chdir(PWD)
    if not missing_apps:
        print('The cordova apps are complete, no need to build.')
        return
    else:
        for app in missing_apps:
            print(app)
            cmd = './build_cordova_apps.py '
            cmd += '-v {xwalk_version} '.format(xwalk_version = xwalk_version)
            cmd += '-a {arch} '.format(arch = arch)
            cmd += '-m {mode} '.format(mode = mode)
            cmd += '-n {name}'.format(name = app)
            os.system(cmd)

def main():

    parser = argparse.ArgumentParser(description = \
                                'List all the missing cordova apps for ' \
                                'a cordova test suite release.')
    parser.add_argument('-v', '--version', type = str, required = True,
                        help =  'specify the Crosswalk version')
    parser.add_argument('-b', '--branch', type = str,
                        help = 'specify the branch of Crosswalk manually')
    parser.add_argument('-m', '--mode', type = str, required = True,
                        help =  'specify the cordova app mode with ' \
                                'cordova plugin Crosswalk Webview.')
    parser.add_argument('-a', '--arch', type = str, required = True,
                        help =  'specify the CPU architecture of cordoa app ' \
                                'with cordova plugin Crosswalk Webview')

    args = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    xwalk_branch = None
    if not args.branch:
        xwalk_branch = xwalk.get_xwalk_branch(args.version)
    else:
        xwalk_branch = args.branch

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

    missing_cordova_apps = get_missing_cordova_apps(configuration,
                                                    xwalk_branch,
                                                    args.version,
                                                    args.mode,
                                                    args.arch)
    build_missing_cordova_apps(missing_cordova_apps,
                            configuration,
                            xwalk_branch,
                            args.version,
                            args.mode,
                            args.arch)


if __name__ == '__main__':
    global PWD
    PWD = os.getcwd()
    main()
