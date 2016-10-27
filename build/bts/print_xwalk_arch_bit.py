#!/usr/bin/env python3

import sys


def print_xwalk_arch_bit(arch):
    if arch.endswith('64'):
        print('64')
    else:
        print('32')


if __name__ == '__main__':
    print_xwalk_arch_bit(sys.argv[1])
