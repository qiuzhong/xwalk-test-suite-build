#!/usr/bin/env python3

'''List the test suite names in a crosswalk-test-suite repo
with specific names.
Usage:
    ./list_specific_tc.py -t "ios" -d <path/to/ctsrepo>
'''

import os
import sys
import argparse


def list_specific_tc(cts_dir, tag):
    '''Return all the test suites with the tag in the names'''
    specific_tc = []

    for d in os.listdir(cts_dir):
        sub_dir = d
        abs_sub_dir = os.path.join(cts_dir, sub_dir)
        if os.path.isdir(abs_sub_dir):
            for tc_dir in os.listdir(abs_sub_dir):
                if os.path.isdir(os.path.join(abs_sub_dir, tc_dir)) and \
                    tag in tc_dir:
                    # print(tc_dir)
                    specific_tc.append(tc_dir)

    return specific_tc


def main():

    parser = argparse.ArgumentParser(description = 'List all the test suites' \
                                                    ' with a specific tag name'
                                    )
    parser.add_argument('-d', '--ctsdir', type = str, required = True,
                        help = 'specify the root directory of a ' \
                                'crosswalk-test-suite repo')
    parser.add_argument('-t', '--tag', type = str, required = True,
                        help = 'specify the tag name to search')

    args = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    for tc in list_specific_tc(os.path.expanduser(args.ctsdir), args.tag):
        print(tc)


if __name__ == '__main__':
    main()
