#!/usr/bin/env python3

import os
import sys
import json
import argparse


class CTSVersion:

    def __init__(self, cts_ver_path):
        self.version_path = cts_ver_path
        self.version_json = None

    def read_version(self):        
        data = None
        with open(self.version_path) as f:
            data = f.read()

        if data is not None:
            print(data)

        try:
            self.version_json = json.loads(data)
        except json.JSONDecodeError:
            sys.stderr.write('Failed to load {version_path}' \
                             ' as JSON format!\n'.format(
                            version_path = self.version_path))
            sys.exit(1)


    def update_version(self, xwalk_version, branch = 'beta'):
        if xwalk_version.endswith('.0'):
            branch = 'canary'

        if self.version_json['main-version'] == xwalk_version and \
            self.version_json['crosswalk-branch'] == branch:
            print('No need to update the version and branch.')
            return

        self.version_json['crosswalk-branch'] = branch
        self.version_json['main-version'] = xwalk_version

        updated_version_str = '{\n'
        updated_version_str += ' ' * 4
        updated_version_str += '"main-version": "{main_version}",\n'.format(
                                main_version = xwalk_version)
        updated_version_str += ' ' * 4
        updated_version_str += '"crosswalk-branch": "{branch}",\n'.format(
                                branch = branch)
        updated_version_str += ' ' * 4
        updated_version_str += '"release-version": "1"\n'
        updated_version_str += '}\n'

        try:
            with open(self.version_path, 'w') as f:
                f.write(updated_version_str)

            print(updated_version_str)                
        except Exception:
            self.recovery_version()


    def recovery_version(self):
        version_dir = os.path.dirname(self.version_path)
        os.chdir(version_dir)
        os.system('git checkout -- VERSION')


def update_cts_version(cts_dir, xwalk_version):
    '''Update the VERSION in cts_dir with the xwalk_version'''
    cts_version_path = os.path.join(cts_dir, 'VERSION')

    if not os.path.exists(cts_version_path):
        sys.stderr.write('VERSION file in {cts_version_path}' \
                         ' does not exists, check it first!\n'.format(
                        cts_version_path = cts_version_path))
        sys.exit(1)

    ctsver = CTSVersion(cts_version_path)
    print('Before update the version -->')
    ctsver.read_version()
    print('After update teh version -->')
    ctsver.update_version(xwalk_version)



def main():
    
    parser = argparse.ArgumentParser(description = \
            'Update the content of VERSION in a crosswalk-test-suite repo.')
    parser.add_argument('-v', '--version', type = str, 
                        help = 'Specify the crosswalk version')
    parser.add_argument('-b', '--branch', type = str, default = 'beta', 
                        help = 'Specify if the branch is beta/canary/stable')
    parser.add_argument('-d', '--ctsdir', type = str, 
                        help = 'Specify the root directory of a CTS repo')

    args = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    if not args.version:
        sys.stderr.write('No crosswalk version specified!\n')
        sys.exit(1)

    conf_filename = __file__.replace('.py', '.json')
    config = None
    cts_dir = None
    if args.ctsdir:
        cts_dir = os.path.expanduser(args.ctsdir)
    else:
        try:
            with open(conf_filename) as fp:
                config = json.load(fp)
        except IOError:
            sys.stderr.write('Failed to open {conf_filename}!\n'.format(
                conf_filename = conf_filename))
            sys.exit(1)

        cts_dir = os.path.expanduser(config.get('cts_dir'))

    if cts_dir:
        print('Update {cts_dir} with version {version}'.format(
                cts_dir = cts_dir, 
                version = args.version))
        update_cts_version(cts_dir, args.version)


if __name__ == '__main__':
    main()