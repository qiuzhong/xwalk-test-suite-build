#!/usr/bin/env python3

import sys


def print_xwalk_branch_num(xwalk_version):
    print(xwalk_version.strip().split('.')[0])


if __name__ == '__main__':
    print_xwalk_branch_num(sys.argv[1])
