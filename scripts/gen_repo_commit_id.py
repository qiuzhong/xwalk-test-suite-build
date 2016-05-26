#!/usr/bin/env python3

'''
Generate a file named as a commit id and its content.
'''

import os
import sys
import argparse
import subprocess


def gen_commit_id(repodir, destdir):
    git_cmd = ['git', 'log', '-1', '--pretty=oneline']
    p = subprocess.Popen(git_cmd,
                        stdout = subprocess.PIPE,
                        stderr = subprocess.STDOUT
                        )
    p.wait()
    git_log = p.stdout.read().strip().split()[0].decode()

    if not git_log:
        sys.stderr.write('Failed to get commit id information!\n')
        return False

    print(git_log)
    with open(os.path.join(destdir, git_log), 'w') as f:
        f.write(git_log + '\n')

    return True


def main():

    parser = argparse.ArgumentParser(description = 'Generate a file named '
                                                    'as a commit id')
    parser.add_argument('-r', '--repodir', type = str,
                        help = 'specify the root directory of a repo')
    parser.add_argument('-d', '--destdir', type = str,
                        help = 'specify the directory where the commit id' \
                                'file is stored.')
    args = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    if not args.repodir:
        sys.stderr.write('No repo directory specified, exit with 1!\n')
        sys.exit(1)

    destdir = None
    if not args.destdir:
        destdir = os.getcwd()
    else:
        destdir = args.destdir

    gen_commit_id(os.path.expanduser(args.repodir), destdir)


if __name__ == '__main__':
    main()
