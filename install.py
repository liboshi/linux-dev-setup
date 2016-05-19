#!/usr/bin/env python

'''
TODO:
    o Add one process to clone linux-dev-setup, this is just used by myself.
    o FIXED: Install vim plugins after install Vundle.vim automatically.
'''

import os
import re
import sys
import platform
import logging
import subprocess

log = logging.getLogger(__name__)

def which_dist():
    dist_name = platform.dist()[0]
    if re.search(r'Ubuntu|debian', dist_name):
        return 'debian'
    else:
        return 'redhat'

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

def install_tmux():
    log.info('>>> Install tmux')
    pkg_cmd = 'apt-get'
    dist_name = which_dist()
    if dist_name != 'debian':
        pkg_cmd = 'yum'
    subprocess.call(r'sudo {0} install -y tmux'.format(pkg_cmd), shell = True)

def install_vim_plugins():
    log.info('>>> Install vim plugins')
    subprocess.call(r'vim +PluginInstall +qall', shell = True)

def link_file(original_filename, symlink_filename):
    original_path = os.path.join(os.getcwd(), original_filename)
    symlink_path  = os.path.expanduser(symlink_filename)
    if os.path.exists(symlink_path):
        os.unlink(symlink_path)
    os.symlink(original_path, symlink_path)

LINKED_FILE = {
        'vimrc':         r'~/.vimrc',
        'vimrc.bundles': r'~/.vimrc.bundles',
        'tmux.conf':     r'~/.tmux.conf'}

def main():
    log.info('>>> Start...')
    install_tmux()
    install_github_bundle('VundleVim', 'Vundle.vim')
    for k, v in LINKED_FILE.iteritems():
        link_file(k, v)
    # Install vim plugins
    install_vim_plugins()

if __name__ == '__main__':
    main()
