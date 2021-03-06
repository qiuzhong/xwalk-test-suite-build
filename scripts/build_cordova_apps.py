#!/usr/bin/env python3


import os
import sys
import json
import argparse

import xwalk
import cordova


def build_cordova_app(cts_dir, xwalk_branch, xwalk_version, mode, arch, name,
                    commandline_only = False, putonotcqa = False):

    cca_build = False
    if name == 'CIRC' or name == 'Eh':
        cca_build = True
    cordova_builder = cordova.CordovaBuilder(cts_dir,
                                            xwalk_branch, xwalk_version,
                                            mode, arch,
                                            commandline_only,
                                            putonotcqa)
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
    parser.add_argument('-a', '--arch', type = str, required = True,
                        help =  'specify the CPU architecture, ' \
                                'arm/arm64/x86/x86_64')
    parser.add_argument('-m', '--mode', type = str, required = True,
                        help =  'specify the crosswalk application mode, ' \
                                'embedded/shared')
    parser.add_argument('-n', '--name', type = str, required = True,
                        help =  'specify the cordova app name')
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

    if not xwalk.check_xwalk_version_valid(args.version):
        sys.stderr.write('Invalid Crosswalk version!\n')
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
    #if args.arch.endswith('64'):
    #    cts_dir += '-x64'

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
                    args.name,
                    args.commandline_only,
                    args.putonotcqa)


if __name__ == '__main__':
    main()
