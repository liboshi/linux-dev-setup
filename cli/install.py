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
import logging
import subprocess

# Import self modules
from cli import config
from cli import colors

from optparse import OptionParser

from .formatter import Formatter
from .formatter import ConsoleWarningFormatter
from .utils import which_dist
from .utils import get_pkg_cmd

# Get commandline arguments
parser = OptionParser()
parser.add_option('-v', '--verbose', dest='verbose',
                  help = 'make lots of noise [non-default]')
(opts, args) = parser.parse_args()
options = vars(opts)

log = logging.getLogger(__name__)
console_handler = logging.StreamHandler(sys.stderr)

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
    log.info('>>> Install {0}'.format(colors.blue(app_name)))
    subprocess.call(r'sudo {0} install -y {1} >/dev/null'.format(pkg_cmd, app_name),
                    shell = True)

def install_vim_plugins():
    log.info('>>> Install ' + colors.blue('vim plugins'))
    subprocess.call(r'vim +PluginInstall +qall', shell = True)

def link_file(original_filename, symlink_filename):
    original_path = os.path.join(os.getcwd(), original_filename)
    symlink_path  = os.path.expanduser(symlink_filename)
    if os.path.exists(symlink_path):
        os.unlink(symlink_path)
    os.symlink(original_path, symlink_path)

def install():
    setup_logging()
    setup_console_handler(console_handler, options.get('--verbose'))
    log.info(colors.red('>>>') +' Start...')
    pkg_cmd = get_pkg_cmd()
    # Install applications
    for app in config.INSTALL_APPS:
        install_app(pkg_cmd, app)
    for k, v in config.LINKED_FILE.iteritems():
        link_file(k, v)
    # Install vim plugins
    install_github_bundle('VundleVim', 'Vundle.vim')
    install_vim_plugins()
