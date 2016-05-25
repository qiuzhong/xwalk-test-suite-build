#!/usr/bin/env python3


def get_xwalk_branch(xwalk_version):

    xwalk_branch = 'beta'
    if xwalk_version.endswith('.0'):
        xwalk_branch = 'master'

    return xwalk_branch