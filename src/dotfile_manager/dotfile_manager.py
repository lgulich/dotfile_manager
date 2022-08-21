from pathlib import Path
import argparse
import os

from dotfile_manager.repo import DotfilesRepo
from dotfile_manager.version import __version__
from dotfile_manager.config import DOTFILES_PATH_ENV_VARIABLE


def main():
    parser = argparse.ArgumentParser(description='Tool for managing dotfiles for linux and macos.')
    parser.add_argument('-d',
                        '--dotfiles',
                        type=str,
                        default='',
                        help='Path to the dotfiles repository')
    parser.add_argument('-v',
                        '--version',
                        action='version',
                        version=__version__,
                        help='Print the version')

    verb_parser = parser.add_subparsers(dest='verb')
    verb_parser.required = True

    _ = verb_parser.add_parser('setup', help='Setup dotfiles')
    _ = verb_parser.add_parser('install', help='Install dependencies of dotfiles')

    args = parser.parse_args()

    # If dotfiles path is not set via CLI we fallback to env variable.
    dotfiles_path = Path(args.dotfiles)
    if dotfiles_path == '':
        if DOTFILES_PATH_ENV_VARIABLE in os.environ:
            dotfiles_path = Path(os.environ[DOTFILES_PATH_ENV_VARIABLE])
        else:
            dotfiles_path = Path(os.getcwd())

    dotfiles = DotfilesRepo(dotfiles_path)
    if args.verb == 'install':
        dotfiles.install()
        return

    if args.verb == 'setup':
        dotfiles.setup()
        return
