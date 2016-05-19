#!/usr/bin/env python

'''
TODO:
    o Add one process to clone linux-dev-setup, this is just used by myself.
    o FIXED: Install vim plugins after install Vundle.vim.
'''

import os
import sys
import logging
import subprocess

log = logging.getLogger(__name__)

def make_vim_plugin_folder():
    vim_plugin_folder = os.path.expanduser(r'~/.vim/bundle')
    if not os.path.exists(vim_plugin_folder):
        os.makedirs(vim_plugin_folder)
    else:
        log.info('>>> Plugin folder exists...')

def install_github_bundle(user, package):
    if not os.path.exists(os.path.expanduser("~/.vim/bundle/{0}".format(package))):
        subprocess.call(r'git clone https://github.com/{0}/{1}'.format(user, package),
                        shell = True)

def install_tmux():
    log.info('>>> Install tmux')
    subprocess.call(r'sudo apt-get install -y tmux', shell = True)

def link_file(original_filename, symlink_filename):
    original_path = os.path.expanduser(original_filename)
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
    install_github_bundle('VundleVim', 'Vundle.vim.git')
    for k, v in LINKED_FILE.iteritems():
        link_file(k, v)
    # Install vim plugins
    print('''>>> Install vim plugins:
    Please start vim and then run following commands:
      ":PluginInstall"''')

if __name__ == '__main__':
    main()
