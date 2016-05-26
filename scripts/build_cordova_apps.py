#!/usr/bin/env python3


import os
import sys
import json
import argparse

import xwalk
import cordova


def build_cordova_app(cts_dir, xwalk_branch, xwalk_version, mode, arch, name):

    cca_build = False
    if name == 'CIRC' or name == 'Eh':
        cca_build = True
    cordova_builder = cordova.CordovaBuilder(cts_dir,
                                            xwalk_branch, xwalk_version,
                                            mode, arch)
    cordova_builder.set_dest_dir()
    cordova_builder.recovery_cordova_plugin_xwalk_webview()
    cordova_builder.update_cordova_plugin_xwalk_webview(cca_build)
    cordova_builder.build_cordova(name, build_type = 'apps')
    cordova_builder.recovery_cordova_plugin_xwalk_webview()


def main():

    parser = argparse.ArgumentParser(description = \
                                    'Build a cordova sample app.')
    parser.add_argument('-v', '--version', type = str,
                        help =  'Specify the crosswalk version')
    parser.add_argument('-a', '--arch', type = str, default = 'arm',
                        help =  'specify the CPU architecture, ' \
                                'arm/arm64/x86/x86_64')
    parser.add_argument('-m', '--mode', type = str, default = 'embedded',
                        help =  'specify the crosswalk application mode, ' \
                                'embedded/shared')
    parser.add_argument('-n', '--name', type = str,
                        help =  'specify the cordova app name')
    parser.add_argument('-q', '--putonotcqa', action = 'store_true',
                        default = True,
                        help =  'specify if put on the cordova apps to ' \
                                'otcqa server after copying to ' \
                                'data directory')

    args = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    if not args.version:
        sys.stderr.write('No Crosswalk version specified, exit with 1\n')
        sys.exit(1)

    if not args.name:
        sys.stderr.write('No Crosswalk name specified, exit with 1\n')
        sys.exit(1)

    if not args.mode:
        sys.stderr.write('No app mode specified, exit with 1\n')
        sys.exit(1)

    if not args.arch:
        sys.stderr.write('No app arch specified, exit with 1\n')
        sys.exit(1)

    cts_json_file = 'update_cts_version.json'
    cts_json = None
    with open(cts_json_file) as f:
        cts_json = json.load(f)

    try:
        branch_num = args.version.split('.')[0]
    except Exception:
        sys.stderr.write('Failed to get the branch number from ' \
                        '{xwalk_version}'.format(
                        xwalk_version = args.version))
        sys.exit(1)

    xwalk_branch = xwalk.get_xwalk_branch(args.version)
    cts_dir = os.path.expanduser(cts_json.get(
                                xwalk_branch).get(
                                branch_num).get(
                                'cts_dir'))
    if args.arch.endswith('64'):
        cts_dir += '-x64'
    print(cts_dir)

    version_json = None
    with open(os.path.join(cts_dir, 'VERSION')) as f:
        version_json = json.load(f)
    xwalk_version = version_json.get('main-version')

    assert args.version == xwalk_version, \
        'CTS VERSION does not match args.version'

    build_cordova_app(cts_dir,
                    xwalk_branch,
                    xwalk_version,
                    args.mode,
                    args.arch,
                    args.name)


if __name__ == '__main__':
    main()