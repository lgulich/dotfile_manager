from pathlib import Path
import argparse
import os

from dotfile_manager.repo import Repo
from dotfile_manager.version import __version__
from dotfile_manager.config import DOTFILES_PATH_ENV_VARIABLE


def select_dotfiles_path(cli_argument: str) -> Path:
    """
    Select the correct dotfiles path by falling back to the config with the highest priority.
    Priority is cli_argument > environment variable > current working directory.
    """
    if cli_argument:
        return Path(cli_argument)

    if DOTFILES_PATH_ENV_VARIABLE in os.environ:
        return Path(os.environ[DOTFILES_PATH_ENV_VARIABLE])

    return Path(os.getcwd())


def main():
    parser = argparse.ArgumentParser(description='Tool for managing dotfiles for linux and macos.')
    parser.add_argument('-d',
                        '--dotfiles',
                        type=str,
                        default=None,
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

    dotfiles_path = select_dotfiles_path(args.dotfiles)

    dotfiles = Repo(dotfiles_path)
    if args.verb == 'install':
        dotfiles.install()
        return

    if args.verb == 'setup':
        dotfiles.setup()
        return
