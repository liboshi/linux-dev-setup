#!/usr/bin/env python

'''
TODO:
    o Add one process to clone linux-dev-setup, this is just used by myself.
    o FIXED: Install vim plugins after install Vundle.vim automatically.
    o FIXED: Install build-essential in order to build YouCompleteMe.
'''

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
import re
import sys
import platform
import logging
import subprocess

from optparse import OptionParser

from .formatter import Formatter
from .formatter import ConsoleWarningFormatter

# Get commandline arguments
parser = OptionParser()
parser.add_option('-v', '--verbose', dest='verbose',
                  help = 'make lots of noise [non-default]')
(opts, args) = parser.parse_args()
options = vars(opts)

log = logging.getLogger(__name__)
console_handler = logging.StreamHandler(sys.stderr)

# Configuration files definitions
LINKED_FILE = {
        'vimrc':           r'~/.vimrc',
        'vimrc.bundles':   r'~/.vimrc.bundles',
        'tmux.conf':       r'~/.tmux.conf',
        'tmux.conf.local': r'~/.tmux.conf.local'}

def setup_logging():
    root_logger = logging.getLogger()
    root_logger.addHandler(console_handler)
    root_logger.setLevel(logging.DEBUG)

    # Disable requests logging
    logging.getLogger('requests').propagate = False

def setup_console_handler(handler, verbose):
    if handler.stream.isatty():
        format_class = ConsoleWarningFormatter
    else:
        format_class = logging.Formatter

    if verbose:
        handler.setFormatter(format_closs('%(name)s.%(funcName)s:%(message)'))
    else:
        handler.setFormatter(format_class())
        handler.setLevel(logging.INFO)

def which_dist():
    dist_name = platform.dist()[0]
    if re.search(r'Ubuntu|debian', dist_name):
        return 'debian'
    else:
        return 'redhat'

def get_pkg_cmd():
    pkg_cmd = 'apt-get'
    dist_name = which_dist()
    if dist_name != 'debian':
        pkg_cmd = 'yum'
    return pkg_cmd

def make_vim_plugin_folder():
    vim_plugin_folder = os.path.expanduser(r'~/.vim/bundle')
    if not os.path.exists(vim_plugin_folder):
        try:
            os.makedirs(vim_plugin_folder)
        except OSError as err:
            log.error(err)
    else:
        log.info('>>> Plugin folder exists...')

def install_github_bundle(user, package):
    dest_clone_path = os.path.expanduser(r'~/.vim/bundle/{0}'.format(package))
    if not os.path.exists(os.path.expanduser("~/.vim/bundle/{0}".format(package))):
        subprocess.call(r'git clone \
                          https://github.com/{0}/{1}.git \
                          {2}'.format(user, package, dest_clone_path),
                        shell = True)

def install_app(pkg_cmd, app_name):
    log.info('>>> Install {0}'.format(app_name))
    subprocess.call(r'sudo {0} install -y {1}'.format(pkg_cmd, app_name),
                    shell = True)

def install_vim_plugins():
    log.info('>>> Install vim plugins')
    subprocess.call(r'vim +PluginInstall +qall', shell = True)

def link_file(original_filename, symlink_filename):
    original_path = os.path.join(os.getcwd(), original_filename)
    symlink_path  = os.path.expanduser(symlink_filename)
    if os.path.exists(symlink_path):
        os.unlink(symlink_path)
    os.symlink(original_path, symlink_path)

def main():
    setup_logging()
    setup_console_handler(console_handler, options.get('--verbose'))
    log.info('>>> Start...')
    pkg_cmd = get_pkg_cmd()
    install_app(pkg_cmd, 'tmux')
    install_app(pke_cmd, 'git')
    install_app(pkg_cmd, 'cmake')
    install_app(pke_cmd, 'build-essential')
    install_github_bundle('VundleVim', 'Vundle.vim')
    for k, v in LINKED_FILE.iteritems():
        link_file(k, v)
    # Install vim plugins
    install_vim_plugins()
