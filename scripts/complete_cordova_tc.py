#!/usr/bin/env python3

import os
import sys
import glob
import json
import argparse
import collections

import xwalk


def get_missing_cordova_tc(configuration,
                            xwalk_branch,
                            xwalk_version,
                            mode,
                            arch,
                            commandline_only = False,
                            cordova_prefix = 'cordova4.x'):
    '''Check the missing cordova test suites and return a dict.'''
    missing_cordova_tc = collections.defaultdict(list)
    cordova_config = None
    try:
        with open('cordova_tc.json') as f:
            cordova_config = json.load(f)
    except Exception:
        sys.stderr.write('Failed to read json configuration from ' \
                         'cordova_tc.json, exit with 1\n')
        sys.exit(1)

    if not cordova_config:
        sys.write.write('Cordova configuration is empty, exit with 1\n')
        sys.exit(1)

    branch_num = xwalk_version.split('.')[0]
    all_cordova_tc = cordova_config.get(branch_num)
    if not all_cordova_tc:
        sys.stderr.write('Cordova test suite list is empty, exit with 1\n')
        sys.exit(1)

    cordova_tc_dir = os.path.join(configuration.get('jiajia_dir_prefix'),
                                    xwalk_branch,
                                    xwalk_version,
                                    cordova_prefix + '-' + mode,
                                    arch)
    if not os.path.exists(cordova_tc_dir):
        sys.stderr.write('{cordova_tc_dir} does not exist!\n'.format(
                        cordova_tc_dir = cordova_tc_dir))
        return all_cordova_tc

    os.chdir(cordova_tc_dir)
    present_cordova_tc = [tc.replace('-{xwalk_version}-1.cordova.zip'.format(
                                        xwalk_version = xwalk_version
                                    ), '')
                        for tc in glob.glob('*.cordova.zip')]
    present_cordova_tc.sort()
    for tc_field, tc_name_list in all_cordova_tc.items():
        for tc_name in tc_name_list:
            if tc_name not in present_cordova_tc:
                missing_cordova_tc[tc_field].append(tc_name)

    if not missing_cordova_tc:
        print('No missing test suites')
    for tc_field, missing_cordova_tc_list in missing_cordova_tc.items():
        for missing_tc_name in missing_cordova_tc_list:
            if commandline_only:
                print(os.path.join(tc_field, missing_tc_name))

    return missing_cordova_tc


def build_missing_cordova_tc(missing_cordova_tc,
                            configuration,
                            xwalk_branch,
                            xwalk_version,
                            mode,
                            arch,
                            commandline_only,
                            putonotcqa):
    if not missing_cordova_tc:
        return

    global PWD
    print('cd {pwd}'.format(pwd = PWD))
    os.chdir(PWD)
    for tc_field, missing_tc_name_list in missing_cordova_tc.items():
        for missing_tc_name in missing_tc_name_list:
            cmd = './build_cordova_tc.py '
            cmd += '-v {xwalk_version} '.format(xwalk_version = xwalk_version)
            cmd += '-a {arch} '.format(arch = arch)
            cmd += '-m {mode} '.format(mode = mode)
            cmd += '-n {name}'.format(name = os.path.join(tc_field,
                                    missing_tc_name))
            if putonotcqa:
                cmd += ' -q'
            if commandline_only:
                print(cmd)
            else:
                os.system(cmd)


def main():
    '''Enter to the build entry'''
    parser = argparse.ArgumentParser(description = \
                                        'List all the missing cordova' \
                                        ' test suites for a cordova release.')
    parser.add_argument('-v', '--version', type = str, required = True,
                        help = 'specify the Crosswalk version')
    parser.add_argument('-b', '--branch', type = str,
                        help = 'specify the branch of Crosswalk manually')
    parser.add_argument('-m', '--mode', type = str, required = True,
                        help =  'specify the cordova test suites mode with ' \
                                'cordova plugin Crosswalk Webview.')
    parser.add_argument('-a', '--arch', type = str, required = True,
                        help =  'specify the CPU architecture of ' \
                                'cordoa test suites with ' \
                                'cordova plugin Crosswalk Webview')
    parser.add_argument('-c', '--commandline_only', action = 'store_true',
                        help = 'specify if print commandline only(no build)')
    parser.add_argument('-q', '--putonotcqa', action = 'store_true',
                        default = False,
                        help =  'specify if put on the cordova apps to ' \
                                'otcqa server after copying to ' \
                                'data directory')
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

    missing_cordova_tc = get_missing_cordova_tc(configuration,
                                                xwalk_branch,
                                                args.version,
                                                args.mode,
                                                args.arch,
                                                args.commandline_only)
    build_missing_cordova_tc(missing_cordova_tc,
                            configuration,
                            xwalk_branch,
                            args.version,
                            args.mode,
                            args.arch,
                            args.commandline_only,
                            args.putonotcqa)

if __name__ == '__main__':
    global PWD
    PWD = os.getcwd()
    main()
