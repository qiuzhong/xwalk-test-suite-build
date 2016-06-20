#!/usr/bin/env python3

import os
import sys
import json
import argparse

import xwalk


def check(path):
    if os.path.exists(path):
        print('{path} already exists! - OK'.format(path=path))
    else:
        print('{path} does not exist! - NOK'.format(path=path))


def check_xwalk_sdk(args):

    if not hasattr(args, 'version'):
        sys.stderr.write('no -v or --version option specified ' \
                        'in command line!\n')
        sys.exit(1)

    if not args.version:
        sys.stderr.write('Please specify a valid crosswalk version value!\n')
        sys.exit(1)

    config = None
    try:
        with open('config.json') as fp:
            config = json.load(fp)
    except Exception:
        sys.stderr.write('Failed to open config.json, exit!\n')
        sys.exit(1)

    pkg_tools_dir = None
    pkg_tools_dir64 = None
    xwalk_zip_dir = None
    if config:
        pkg_tools_dir = config.get('pkg_tools_dir')
        pkg_tools_dir64 = config.get('pkg_tools_dir64')
        xwalk_zip_dir = os.path.expanduser(config.get('xwalk_zip_dir'))

    if pkg_tools_dir:
        xwalk = os.path.join(pkg_tools_dir, 'crosswalk-{version}'.format(
                                                    version = args.version))
        check(xwalk)

        xwalk_embedded_aar = os.path.join(pkg_tools_dir,
                                        'crosswalk-{version}.aar'.format(
                                                    version = args.version))
        check(xwalk_embedded_aar)

        xwalk_shared_aar = os.path.join(pkg_tools_dir,
                                    'crosswalk-shared-{version}.aar'.format(
                                                    version = args.version))
        check(xwalk_shared_aar)

        xwalk_apks_arm = os.path.join(pkg_tools_dir,
                                    'crosswalk-apks-{version}-arm'.format(
                                                    version = args.version))
        check(xwalk_apks_arm)
        xwalk_test_apks_arm = os.path.join(pkg_tools_dir,
                                    'crosswalk-test-apks-{version}-arm'.format(
                                                    version = args.version))
        check(xwalk_test_apks_arm)
        xwalk_webview_arm = os.path.join(pkg_tools_dir,
                                    'crosswalk-webview-{version}-arm'.format(
                                                    version = args.version))
        check(xwalk_webview_arm)

        xwalk_apks_x86 = os.path.join(pkg_tools_dir,
                                    'crosswalk-apks-{version}-x86'.format(
                                                    version = args.version))
        check(xwalk_apks_x86)
        xwalk_test_apks_x86 = os.path.join(pkg_tools_dir,
                                    'crosswalk-test-apks-{version}-x86'.format(
                                                    version = args.version))
        check(xwalk_test_apks_x86)
        xwalk_webview_x86 = os.path.join(pkg_tools_dir,
                                    'crosswalk-webview-{version}-x86'.format(
                                                    version = args.version))
        check(xwalk_webview_x86)

    if pkg_tools_dir64:
        xwalk64 = os.path.join(pkg_tools_dir64,
                            'crosswalk-{version}-64bit'.format(
                                        version = args.version))
        check(xwalk64)

        xwalk64_embedded_aar = os.path.join(pkg_tools_dir64,
                            'crosswalk-{version}-64bit.aar'.format(
                                        version = args.version))
        check(xwalk64_embedded_aar)

        xwalk_apks_arm64 = os.path.join(pkg_tools_dir64,
                            'crosswalk-apks-{version}-arm64'.format(
                                            version = args.version))
        check(xwalk_apks_arm64)
        xwalk_test_apks_arm64 = os.path.join(pkg_tools_dir64,
                            'crosswalk-test-apks-{version}-arm64'.format(
                                            version = args.version))
        check(xwalk_test_apks_arm64)
        xwalk_webview_arm64 = os.path.join(pkg_tools_dir64,
                            'crosswalk-webview-{version}-arm64'.format(
                                            version = args.version))
        check(xwalk_webview_arm64)

        xwalk_apks_x86_64 = os.path.join(pkg_tools_dir64,
                            'crosswalk-apks-{version}-x86_64'.format(
                                            version = args.version))
        check(xwalk_apks_x86_64)
        xwalk_test_apks_x86_64 = os.path.join(pkg_tools_dir64,
                            'crosswalk-test-apks-{version}-x86_64'.format(
                                            version = args.version))
        check(xwalk_test_apks_x86_64)
        xwalk_webview_x86_64 = os.path.join(pkg_tools_dir64,
                            'crosswalk-webview-{version}-x86_64'.format(
                                            version = args.version))
        check(xwalk_webview_x86_64)

    if xwalk_zip_dir:
        xwalk_zip = os.path.join(xwalk_zip_dir,
                                'crosswalk-{version}.zip'.format(
                                            version = args.version))
        check(xwalk_zip)

        xwalk64_zip = os.path.join(xwalk_zip_dir,
                                'crosswalk-{version}-64bit.zip'.format(
                                            version = args.version))
        check(xwalk64_zip)


def main():
    parser = argparse.ArgumentParser(description = \
                                    'Check if XWalk SDK is available ' \
                                    'on localhost.')
    parser.add_argument('-v', '--version', type = str, required = True,
                        help = 'specify the version of crosswalk')
    args = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    if not xwalk.check_xwalk_version_valid(args.version):
        sys.stderr.write('Invalid Crosswalk version!\n')
        sys.exit(1)

    check_xwalk_sdk(args)


if __name__ == '__main__':
    main()
