#!/usr/bin/env python3

import argparse


def check_xwalk_version_valid(xwalk_version):
    '''Given a specific Crosswalk version, check if the version is valid'''
    versions = xwalk_version.split('.')
    if len(versions) != 4:
        return False

    if len(versions[0]) != 2:
        return False

    if len(versions[1]) != 2:
        return False

    if len(versions[2]) != 3:
        return False

    if len(versions[3]) >= 3:
        return False

    try:
        major = int(versions[0])
        minor = int(versions[1])
        patch = int(versions[2])
        serial = int(versions[3])
    except Exception:
        return False

    return True


def check_params(args):
    params_correct = True
    error_code = None
    erro_msg = None

    if args.branch not in ('canary', 'master', 'beta', 'stable'):
        params_correct = False
        error_code = 101
        error_msg = 'Wrong Crosswalk branch: {branch}, '.format(branch = args.branch) +
                    'branch must be canary/beta/stable!'

    if check_xwalk_version_valid(args.version):
        params_correct = False
        error_code = 201
        error_msg = 'Wrong Crosswalk version: {version}'.format(version = args.version)

    if args.mode not in ('embedded', 'shared'):
        params_correct = False
        error_code = 301
        error_msg = 'Wrong package mode: {mode}, '.format(mdoe = args.mode) +
                    'mode must be embedded/shared'

    if args.arch not in ('arm', 'x86', 'arm64', 'x86_64'):
        params_correct = False
        error_code = 401
        error_msg = 'Wrong arch: {arch}, '.format(arch = args.arch)

    if args.type not in ('apk', 'cordova', 'embeddingapi',
                        'apk-aio', 'cordova-aio'):
        params_correct = False
        error_code = 501
        error_msg = 'Wrong building type: {type}, '.format(type = args.type) +
                    'apk/cordova/embeddingapi/apk-aio/cordova-aio'

    if not params_correct and error_msg:
        html_content = '''<!DOCTYPE html>
        <html>
          <header>
            <title>Error</title>
          </header>
          <body>
            <h1>Failed to build {testsuite} for Crosswalk {version}/{mode}/{arch}!</h1>
            <h2> Reason: {error_code}: {msg}.</h2>
          </body>
        </html>\n'''.format(testsuite = args.name, version = args.version,
                            mode = args.mode, arch = args.arch,
                            error_code = error_code, msg = error_msg)
        with open('error.html', 'w') as fp:
            fp.write(html_content)


def main():
    parser = argparse.ArgumentParser(description = \
                                'Check the params of building a test suite.')
    parser.add_argument('-b', '--branch', type = str, required = True,
                        help = 'specify the crosswalk branch, ' \
                                'canary/beta/stable')
    parser.add_argument('-v', '--version', type = str, required = True,
                        help =  'Specify the crosswalk version')
    parser.add_argument('-n', '--name', type = str, required = True,
                        help =  'specify the test suite name')
    parser.add_argument('-m', '--mode', type = str, required = True,
                        help =  'specify the crosswalk application mode, ' \
                                'embedded/shared')
    parser.add_argument('-a', '--arch', type = str, required = True,
                        help =  'specify the CPU architecture, ' \
                                'arm/arm64/x86/x86_64')
    parse.add_argument('-t', '--type', type = str, required = True,
                        help = 'specify the package type to build, ' \
                                'apk/cordova/embeddingapi/api-aio/cordova-aio')
    parser.add_argument('-c', '--commandline_only', action = 'store_true',
                        help = 'specify if print commandline only(no build)')
    parser.add_argument('-q', '--putonotcqa', action = 'store_true',
                        default = False,
                        help =  'specify if put on the cordova apps to ' \
                                'otcqa server after copying to ' \
                                'data directory')

    args = parser.parse_args()

    check_params(args)


if __name__ == '__main__':
    main()
