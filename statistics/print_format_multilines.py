#!/usr/bin/env python3


def print_format_for_multilines():

    with open('data.txt') as fp:
        data = fp.read()

    lines = data.strip().split('\n')
    for line in lines:
        print('\t\t\t"cordova/%s": {\n\t\t\t\t"android": "tests.full.xml",\n\t\t\t\t"windows":"tests.full.xml"\n\t\t\t},' % (line,))


if __name__ == '__main__':
    print_format_for_multilines()        