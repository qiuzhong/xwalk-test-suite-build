#!/usr/bin/env python3

import sys


def get_xwalk_branch(xwalk_version):
    '''Get the xwalk branch from a version
    if the branch is master, the last number in the version is always 0
    if the branch is beta, it is likely to change to be stable branch.
    '''
    xwalk_branch = 'beta'
    if xwalk_version.endswith('.0'):
        xwalk_branch = 'master'

    return xwalk_branch


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


def get_xwalk_branch_num(xwalk_version):
    '''Get the xwalk branch number from a version
    For example, version is 18.48.477.13, the branch number is 18
    '''
    branch_num = None
    try:
        branch_num = xwalk_version.strip().split('.')[0]
    except Exception:
        sys.stderr.write('Invalid xwalk version format: ' \
                        '{xwalk_version}'.format(
                        xwalk_version = xwalk_version))

    return branch_num
