#!/usr/bin/env python

'''
This file is used for configuration.
'''

# Configuration files definitions
LINKED_FILE = {
        'muttrc':          r'~/.muttrc',
        'vimrc':           r'~/.vimrc',
        'vimrc.bundles':   r'~/.vimrc.bundles',
        'tmux.conf':       r'~/.tmux.conf',
        'tmux.conf.local': r'~/.tmux.conf.local',
        'bashrc':          r'~/.bashrc',
        'profile':         r'~/.profile',
        'gitconfig':       r'~/.gitconfig'}

INSTALL_APPS = ['vim', 'ctags', 'tmux', 'git', 'cmake', 'gdb', 'clang',
                'build-essential', 'silversearcher-ag']
