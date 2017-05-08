#!/usr/bin/env python

'''
This script is used to cleanup the installation.
'''

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import logging
import subprocess

# Import self modules
from .utils import which_dist
from .utils import get_pkg_cmd

log = logging.getLogger(__name__)
console_handler = logging.StreamHandler(sys.stderr)

def setup_logging():
    root_logger = logging.getLogger()
    root_logger.addHandler(console_handler)
    root_logger.setLevel(logging.DEBUG)

    # Disable requests logging
    logging.getLogger('requests').propagate = False

def unisntall_app(pkg_cmd, app_name):
    log.info('>>> Uninstall {0}'.format(app_name))
    subprocess.call(r'sudo {0} purge -y {1}'.format(pkg_cmd, app_name),
                    shell = True)

def unlink_file(symlink_filename):
    symlink_path = os.path.expanduser(symlink_filename)
    if os.path.exists(symlink_path):
        os.unlink(symlink_path)

def remove_vim_plugin_folder():
    vim_plugin_folder = os.path.expanduser(r'~/.vim/bundle')
    if not os.path.exists(vim_plugin_folder):
        log.info('>>> No need to remove vim folder...')
    else:
        os.removedirs(vim_plugin_folder)

def uninstall():
    setup_logging()
    log.info('>>> Uninstall start...')
    pkg_cmd = get_pkg_cmd()
    log.info('>>> Unlink configuration files...')
    for k, v in config.LINKED_FILE.iteritems():
        unlink_file(v)
    log.info('>>> Remove vim folder...')
    remove_vim_plugin_folder()
    log.info('>>> Remove the apps installed by this tool...')
