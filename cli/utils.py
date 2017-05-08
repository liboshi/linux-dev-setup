#!/usr/bin/env python

'''
This file is used for utilities.
'''

from __future__ import obsolute_import
from __future__ import print_function
from __future__ import unicode_literals

def which_dist():
    dist_name = platform.dist()[0]
    if re.search(r'Ubuntu|debian', dist_name):
        return 'debian'
    else:
        return 'redhat'

def get_pkg_cmd():
    pkg_cmd = 'apt'
    dist_name = which_dist()
    if dist_name != 'debian':
        pkg_cmd = 'yum'
    return pkg_cmd

